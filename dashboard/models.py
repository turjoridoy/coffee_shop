from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None, **extra_fields):
        if not phone:
            raise ValueError("The phone field must be set")

        user = self.model(
            phone=phone, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, phone, first_name, last_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, first_name, last_name, password, **extra_fields)


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )

    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_TYPES = [
        ("stockable", "Stockable (Inventory)"),
        ("non_stockable", "Non-Stockable (Instant)"),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    product_type = models.CharField(
        max_length=20, choices=PRODUCT_TYPES, default="non_stockable"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(
        default=0, help_text="Current stock quantity (for stockable products)"
    )
    min_stock_level = models.PositiveIntegerField(
        default=0, help_text="Minimum stock level for alerts"
    )
    is_quick_action = models.BooleanField(
        default=False, help_text="Show this product in Quick Actions section"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category__name", "name"]

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @property
    def is_low_stock(self):
        """Check if stock is below minimum level"""
        return (
            self.product_type == "stockable"
            and self.stock_quantity <= self.min_stock_level
        )

    @property
    def is_out_of_stock(self):
        """Check if product is out of stock"""
        return self.product_type == "stockable" and self.stock_quantity <= 0

    def update_stock(self, quantity_change):
        """Update stock quantity (positive for addition, negative for reduction)"""
        if self.product_type == "stockable":
            self.stock_quantity += quantity_change
            if self.stock_quantity < 0:
                self.stock_quantity = 0
            self.save()


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name="sales"
    )
    customer_name = models.CharField(max_length=100, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} - {self.total_amount}"

    def save(self, *args, **kwargs):
        # Auto-calculate total amount if not provided
        if not self.total_amount:
            self.total_amount = self.quantity * self.unit_price

        # Update stock if this is a new sale and product is stockable
        if not self.pk and self.product.product_type == "stockable":
            self.product.update_stock(-self.quantity)

        super().save(*args, **kwargs)
