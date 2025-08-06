from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Sale, PaymentMethod, Category, User, Product


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "product_type",
        "price",
        "stock_quantity",
        "is_quick_action",
        "is_low_stock",
        "is_active",
    ]
    list_filter = [
        "category",
        "product_type",
        "is_quick_action",
        "is_active",
        "created_at",
    ]
    search_fields = ["name", "category__name"]
    readonly_fields = ["is_low_stock", "is_out_of_stock", "created_at", "updated_at"]
    ordering = ["category__name", "name"]
    list_editable = ["is_quick_action", "is_active"]
    actions = [
        "mark_as_quick_action",
        "remove_from_quick_action",
    ]

    fieldsets = (
        (
            "Product Information",
            {
                "fields": (
                    "name",
                    "category",
                    "product_type",
                    "price",
                )
            },
        ),
        (
            "Inventory Management",
            {
                "fields": (
                    "stock_quantity",
                    "min_stock_level",
                    "is_low_stock",
                    "is_out_of_stock",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Quick Actions",
            {
                "fields": ("is_quick_action",),
                "classes": ("collapse",),
            },
        ),
        (
            "Status",
            {
                "fields": ("is_active",),
            },
        ),
        (
            "System Information",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")

    @admin.action(description="Mark selected products as Quick Actions")
    def mark_as_quick_action(self, request, queryset):
        updated = queryset.update(is_quick_action=True)
        self.message_user(request, f"{updated} products marked as Quick Actions.")

    @admin.action(description="Remove selected products from Quick Actions")
    def remove_from_quick_action(self, request, queryset):
        updated = queryset.update(is_quick_action=False)
        self.message_user(request, f"{updated} products removed from Quick Actions.")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "quantity",
        "unit_price",
        "total_amount",
        "payment_method",
        "customer_name",
        "created_at",
    ]
    list_filter = ["product__category", "payment_method", "created_at"]
    search_fields = ["product__name", "customer_name", "customer_phone"]
    readonly_fields = ["total_amount", "created_at"]
    ordering = ["-created_at"]

    fieldsets = (
        (
            "Product Information",
            {
                "fields": (
                    "product",
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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("product", "payment_method")


# Customize admin site
admin.site.site_header = "Tea Time Admin"
admin.site.site_title = "Coffee Shop Admin"
admin.site.index_title = "Welcome to Coffee Shop Management System"
