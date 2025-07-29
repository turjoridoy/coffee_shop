from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from dashboard.models import Category, PaymentMethod, Product, Sale
import random


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database with initial data...")

        # Create categories
        categories_data = [
            "Coffee",
            "Tea",
            "Snacks",
            "Beverages",
            "Desserts",
        ]

        categories = {}
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name, defaults={"is_active": True}
            )
            categories[cat_name] = category
            if created:
                self.stdout.write(f"Created category: {cat_name}")

        # Create payment methods
        payment_methods_data = [
            "Cash",
            "Card",
            "Mobile Banking",
            "Bkash",
            "Nagad",
        ]

        payment_methods = {}
        for pm_name in payment_methods_data:
            pm, created = PaymentMethod.objects.get_or_create(
                name=pm_name, defaults={"is_active": True}
            )
            payment_methods[pm_name] = pm
            if created:
                self.stdout.write(f"Created payment method: {pm_name}")

        # Create products
        products_data = [
            # Coffee products (non-stockable)
            {
                "name": "Black Coffee",
                "category": "Coffee",
                "price": 30.00,
                "product_type": "non_stockable",
                "is_quick_action": True,
            },
            {
                "name": "Cappuccino",
                "category": "Coffee",
                "price": 45.00,
                "product_type": "non_stockable",
            },
            {
                "name": "Latte",
                "category": "Coffee",
                "price": 50.00,
                "product_type": "non_stockable",
            },
            {
                "name": "Espresso",
                "category": "Coffee",
                "price": 35.00,
                "product_type": "non_stockable",
            },
            {
                "name": "Americano",
                "category": "Coffee",
                "price": 40.00,
                "product_type": "non_stockable",
            },
            # Tea products (non-stockable)
            {
                "name": "Black Tea",
                "category": "Tea",
                "price": 20.00,
                "product_type": "non_stockable",
            },
            {
                "name": "Green Tea",
                "category": "Tea",
                "price": 25.00,
                "product_type": "non_stockable",
            },
            {
                "name": "Masala Chai",
                "category": "Tea",
                "price": 30.00,
                "product_type": "non_stockable",
                "is_quick_action": True,
            },
            {
                "name": "Lemon Tea",
                "category": "Tea",
                "price": 25.00,
                "product_type": "non_stockable",
            },
            # Snacks (stockable)
            {
                "name": "Samosa",
                "category": "Snacks",
                "price": 15.00,
                "product_type": "stockable",
                "stock_quantity": 50,
                "min_stock_level": 10,
                "is_quick_action": True,
            },
            {
                "name": "Chicken Roll",
                "category": "Snacks",
                "price": 40.00,
                "product_type": "stockable",
                "stock_quantity": 30,
                "min_stock_level": 5,
            },
            {
                "name": "Veg Roll",
                "category": "Snacks",
                "price": 25.00,
                "product_type": "stockable",
                "stock_quantity": 40,
                "min_stock_level": 8,
            },
            {
                "name": "French Fries",
                "category": "Snacks",
                "price": 60.00,
                "product_type": "stockable",
                "stock_quantity": 25,
                "min_stock_level": 5,
            },
            {
                "name": "Chicken Burger",
                "category": "Snacks",
                "price": 80.00,
                "product_type": "stockable",
                "stock_quantity": 20,
                "min_stock_level": 3,
            },
            # Beverages (stockable)
            {
                "name": "Coca Cola",
                "category": "Beverages",
                "price": 25.00,
                "product_type": "stockable",
                "stock_quantity": 100,
                "min_stock_level": 20,
            },
            {
                "name": "Sprite",
                "category": "Beverages",
                "price": 25.00,
                "product_type": "stockable",
                "stock_quantity": 80,
                "min_stock_level": 15,
            },
            {
                "name": "Pepsi",
                "category": "Beverages",
                "price": 25.00,
                "product_type": "stockable",
                "stock_quantity": 90,
                "min_stock_level": 18,
            },
            {
                "name": "Water Bottle",
                "category": "Beverages",
                "price": 15.00,
                "product_type": "stockable",
                "stock_quantity": 150,
                "min_stock_level": 30,
            },
            # Desserts (stockable)
            {
                "name": "Chocolate Cake",
                "category": "Desserts",
                "price": 120.00,
                "product_type": "stockable",
                "stock_quantity": 15,
                "min_stock_level": 3,
            },
            {
                "name": "Ice Cream",
                "category": "Desserts",
                "price": 80.00,
                "product_type": "stockable",
                "stock_quantity": 25,
                "min_stock_level": 5,
            },
            {
                "name": "Pudding",
                "category": "Desserts",
                "price": 60.00,
                "product_type": "stockable",
                "stock_quantity": 20,
                "min_stock_level": 4,
            },
        ]

        products = {}
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    "category": categories[product_data["category"]],
                    "price": product_data["price"],
                    "product_type": product_data["product_type"],
                    "stock_quantity": product_data.get("stock_quantity", 0),
                    "min_stock_level": product_data.get("min_stock_level", 0),
                    "is_quick_action": product_data.get("is_quick_action", False),
                    "is_active": True,
                },
            )
            products[product_data["name"]] = product
            if created:
                self.stdout.write(f"Created product: {product_data['name']}")

        # Create sample sales
        if Sale.objects.count() == 0:
            # Get some products for sample sales
            sample_products = list(products.values())
            sample_payment_methods = list(payment_methods.values())

            # Create sales for different dates
            for i in range(50):
                # Random date within last 30 days
                days_ago = random.randint(0, 30)
                sale_date = timezone.now() - timedelta(days=days_ago)

                product = random.choice(sample_products)
                payment_method = random.choice(sample_payment_methods)
                quantity = random.randint(1, 5)
                unit_price = float(product.price)
                total_amount = quantity * unit_price

                sale = Sale.objects.create(
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_amount=total_amount,
                    payment_method=payment_method,
                    customer_name=f"Customer {i+1}",
                    customer_phone=f"+8801{random.randint(100000000, 999999999)}",
                    notes=f"Sample sale {i+1}",
                    created_at=sale_date,
                )
                self.stdout.write(f"Created sale: {sale}")

        self.stdout.write(
            self.style.SUCCESS("Successfully seeded database with initial data!")
        )
