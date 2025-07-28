from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create an inactive user for testing"

    def handle(self, *args, **options):
        # Create an inactive user
        user, created = User.objects.get_or_create(
            phone="01700000000",
            defaults={
                "first_name": "Inactive",
                "last_name": "User",
                "is_active": False,
                "password": "testpass123",
            },
        )

        if created:
            user.set_password("testpass123")
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created inactive user: {user.phone} (Password: testpass123)"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Inactive user already exists: {user.phone} (Password: testpass123)"
                )
            )
