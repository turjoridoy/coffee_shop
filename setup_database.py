#!/usr/bin/env python3
"""
Database setup script for Coffee Shop Manager
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()

from django.core.management import call_command
from django.db import connection
import pymysql


def setup_database():
    """Set up database and run migrations"""
    print("🚀 Setting up database for Coffee Shop Manager...")

    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful!")

        # Run migrations
        print("📦 Running migrations...")
        call_command("migrate", verbosity=2)
        print("✅ Migrations completed successfully!")

        # Create superuser
        print("👤 Creating superuser...")
        try:
            call_command("createsuperuser", interactive=False)
            print("✅ Superuser created successfully!")
        except Exception as e:
            print(f"⚠️  Superuser creation failed (might already exist): {e}")

        # Load initial data
        print("📊 Loading initial data...")
        try:
            call_command("seed_data")
            print("✅ Initial data loaded successfully!")
        except Exception as e:
            print(f"⚠️  Data seeding failed: {e}")

        print("🎉 Database setup completed successfully!")

    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("\n🔧 Please check:")
        print("1. Database exists in phpMyAdmin")
        print("2. User credentials are correct")
        print("3. User has proper permissions")
        sys.exit(1)


if __name__ == "__main__":
    setup_database()
