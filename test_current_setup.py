#!/usr/bin/env python3
"""
Test script to verify current server setup
"""

import os
import sys
import platform

print("Content-Type: text/plain")
print()
print("=== Server Environment Test ===")
print(f"Python Version: {platform.python_version()}")
print(f"Platform: {platform.platform()}")
print(f"Current Directory: {os.getcwd()}")
print(f"Python Path: {sys.path[:3]}...")  # Show first 3 paths

# Test Django import
try:
    import django

    print(f"Django Version: {django.get_version()}")
    print("✅ Django is available")
except ImportError as e:
    print(f"❌ Django import failed: {e}")

# Test PyMySQL import
try:
    import pymysql

    print("✅ PyMySQL is available")
except ImportError as e:
    print(f"❌ PyMySQL import failed: {e}")

# Test environment variables
print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set')}")

print("\n=== Server Setup ===")
print("If you can see this, Python CGI is working!")
print("Your Django app should be accessible via passenger_wsgi.py")
