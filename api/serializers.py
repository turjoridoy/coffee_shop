from rest_framework import serializers
from dashboard.models import Sale, PaymentMethod, Category


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name", "is_active"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "is_active"]


class SaleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    payment_method_name = serializers.CharField(
        source="payment_method.name", read_only=True
    )

    class Meta:
        model = Sale
        fields = [
            "id",
            "item_name",
            "category",
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
