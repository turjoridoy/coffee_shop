from django.core.management.base import BaseCommand
from django.core.management import call_command
from dashboard.models import Sale, Product, Category, PaymentMethod


class Command(BaseCommand):
    help = "Reset all data and re-seed the database"

    def handle(self, *args, **options):
        self.stdout.write("Resetting all data...")

        # Delete all sales first
        sales_count = Sale.objects.count()
        Sale.objects.all().delete()
        self.stdout.write(f"Deleted {sales_count} sales")

        # Delete all products
        products_count = Product.objects.count()
        Product.objects.all().delete()
        self.stdout.write(f"Deleted {products_count} products")

        # Delete all categories
        categories_count = Category.objects.count()
        Category.objects.all().delete()
        self.stdout.write(f"Deleted {categories_count} categories")

        # Delete all payment methods
        payment_methods_count = PaymentMethod.objects.count()
        PaymentMethod.objects.all().delete()
        self.stdout.write(f"Deleted {payment_methods_count} payment methods")

        # Re-seed the data
        self.stdout.write("Re-seeding data...")
        call_command("seed_data")

        self.stdout.write(
            self.style.SUCCESS("Successfully reset and re-seeded the database!")
        )
