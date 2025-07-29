from rest_framework import serializers
from dashboard.models import Sale, PaymentMethod, Category, Product


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name", "is_active"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "is_active"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    is_out_of_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "category_name",
            "product_type",
            "price",
            "stock_quantity",
            "min_stock_level",
            "is_low_stock",
            "is_out_of_stock",
            "is_quick_action",
            "is_active",
        ]
        read_only_fields = ["is_low_stock", "is_out_of_stock"]


class SaleSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    category_name = serializers.CharField(
        source="product.category.name", read_only=True
    )
    payment_method_name = serializers.CharField(
        source="payment_method.name", read_only=True
    )

    class Meta:
        model = Sale
        fields = [
            "id",
            "product",
            "product_name",
            "category_name",
            "quantity",
            "unit_price",
            "total_amount",
            "payment_method",
            "payment_method_name",
            "customer_name",
            "customer_phone",
            "notes",
            "created_at",
        ]
        read_only_fields = ["total_amount", "created_at"]
