from django.core.management.base import BaseCommand
from django.core.management import call_command
from dashboard.models import Sale


class Command(BaseCommand):
    help = "Clear existing data and recreate with proper timezone"

    def handle(self, *args, **options):
        self.stdout.write("Clearing existing sales data...")

        # Clear all existing sales
        Sale.objects.all().delete()
        self.stdout.write("Cleared all existing sales")

        # Recreate data with proper timezone
        self.stdout.write("Recreating data with proper timezone...")
        call_command("seed_data")

        self.stdout.write(self.style.SUCCESS("Data reset completed successfully!"))
