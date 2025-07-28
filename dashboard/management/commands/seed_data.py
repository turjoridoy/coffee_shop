from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import Sale, PaymentMethod, Category
from decimal import Decimal
import random
from datetime import timedelta


class Command(BaseCommand):
    help = "Seed initial data for the coffee shop"

    def handle(self, *args, **options):
        self.stdout.write("Seeding initial data...")

        # Create payment methods
        payment_methods = [
            "Cash",
            "Mobile Banking",
            "Card",
            "Digital Wallet",
        ]

        for method_name in payment_methods:
            PaymentMethod.objects.get_or_create(
                name=method_name, defaults={"is_active": True}
            )

        self.stdout.write(f"Created {len(payment_methods)} payment methods")

        # Create categories
        categories = [
            "Coffee",
            "Tea",
            "Snacks",
            "Cold Drinks",
            "Breakfast",
            "Lunch",
            "Desserts",
            "Beverages",
        ]

        for category_name in categories:
            Category.objects.get_or_create(
                name=category_name, defaults={"is_active": True}
            )

        self.stdout.write(f"Created {len(categories)} categories")

        # Create sample sales
        if Sale.objects.count() == 0:
            items = [
                "Espresso",
                "Cappuccino",
                "Latte",
                "Americano",
                "Mocha",
                "Green Tea",
                "Black Tea",
                "Chai Latte",
                "Hot Chocolate",
                "Sandwich",
                "Burger",
                "Pizza",
                "Pasta",
                "Salad",
                "Coca Cola",
                "Sprite",
                "Orange Juice",
                "Lemonade",
                "Pancakes",
                "Omelette",
                "Toast",
                "Cereal",
                "Chicken Rice",
                "Beef Steak",
                "Fish Curry",
                "Vegetable Curry",
                "Chocolate Cake",
                "Ice Cream",
                "Cheesecake",
                "Brownie",
                "Smoothie",
                "Milkshake",
                "Frappuccino",
                "Iced Coffee",
            ]

            payment_methods = list(PaymentMethod.objects.filter(is_active=True))
            categories = list(Category.objects.filter(is_active=True))

            for i in range(20):
                item_name = random.choice(items)
                category = random.choice(categories)
                payment_method = random.choice(payment_methods)
                quantity = random.randint(1, 5)
                unit_price = Decimal(str(random.randint(50, 500)))

                # Create sales with different dates
                if i < 5:  # 5 sales today
                    created_at = timezone.now()
                elif i < 10:  # 5 sales yesterday
                    created_at = timezone.now() - timedelta(days=1)
                elif i < 15:  # 5 sales 2 days ago
                    created_at = timezone.now() - timedelta(days=2)
                else:  # 5 sales 3 days ago
                    created_at = timezone.now() - timedelta(days=3)

                Sale.objects.create(
                    item_name=item_name,
                    category=category,
                    quantity=quantity,
                    unit_price=unit_price,
                    payment_method=payment_method,
                    customer_name=(
                        f"Customer {i+1}" if random.choice([True, False]) else ""
                    ),
                    customer_phone=(
                        f"01{random.randint(100000000, 999999999)}"
                        if random.choice([True, False])
                        else ""
                    ),
                    notes=f"Sample sale {i+1}" if random.choice([True, False]) else "",
                    created_at=created_at,
                )

            self.stdout.write("Created 20 sample sales")
        else:
            self.stdout.write("Sales already exist, skipping...")

        self.stdout.write(self.style.SUCCESS("Data seeding completed successfully!"))
