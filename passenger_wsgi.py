#!/usr/bin/env python3
"""
Passenger WSGI configuration for Hostinger shared hosting
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ["DJANGO_SETTINGS_MODULE"] = "conf.settings"

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()


# Production WSGI application
application = get_wsgi_application()
