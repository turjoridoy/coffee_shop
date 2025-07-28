from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Sale, PaymentMethod, Category, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["phone", "first_name", "last_name", "is_active"]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["phone", "first_name", "last_name"]
    ordering = ["phone"]

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name"]
    ordering = ["id"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [
        "item_name",
        "category",
        "quantity",
        "unit_price",
        "total_amount",
        "payment_method",
        "customer_name",
        "created_at",
    ]
    list_filter = ["category", "payment_method", "created_at"]
    search_fields = ["item_name", "customer_name", "customer_phone"]
    readonly_fields = ["total_amount", "created_at"]
    ordering = ["-created_at"]

    fieldsets = (
        (
            "Item Information",
            {
                "fields": (
                    "item_name",
                    "category",
                    "quantity",
                    "unit_price",
                    "total_amount",
                )
            },
        ),
        ("Payment Information", {"fields": ("payment_method",)}),
        (
            "Customer Information",
            {
                "fields": ("customer_name", "customer_phone", "notes"),
                "classes": ("collapse",),
            },
        ),
        ("System Information", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


# Customize admin site
admin.site.site_header = "Coffee Shop Manager Admin"
admin.site.site_title = "Coffee Shop Admin"
admin.site.index_title = "Welcome to Coffee Shop Management System"
