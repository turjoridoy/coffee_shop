#!/usr/bin/env python3
"""
Database connection test script for Coffee Shop Manager
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()

from django.db import connection
import pymysql


def test_database_connection():
    """Test database connection with different configurations"""
    print("🔍 Testing database connection...")

    # Test configurations
    configs = [
        {
            "name": "Current Django Settings",
            "host": "127.0.0.1",
            "user": "u183730229_root",
            "password": "NtZYc@cuCz6@",
            "database": "u183730229_coffee_shop",
        },
        {
            "name": "Alternative Host",
            "host": "localhost",
            "user": "u183730229_root",
            "password": "NtZYc@cuCz6@",
            "database": "u183730229_coffee_shop",
        },
    ]

    for config in configs:
        print(f"\n📋 Testing: {config['name']}")
        try:
            # Test direct PyMySQL connection
            connection = pymysql.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                port=3306,
                charset="utf8mb4",
            )

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                print(f"✅ Connection successful! Test query result: {result}")

            connection.close()

        except Exception as e:
            print(f"❌ Connection failed: {e}")

    print("\n🔧 Troubleshooting tips:")
    print("1. Check if database 'u183730229_coffee_shop' exists in phpMyAdmin")
    print("2. Verify user 'u183730229_root' has proper permissions")
    print("3. Check if password is correct")
    print("4. Try creating the database manually in phpMyAdmin")
    print("5. Contact Hostinger support if issues persist")


if __name__ == "__main__":
    test_database_connection()
