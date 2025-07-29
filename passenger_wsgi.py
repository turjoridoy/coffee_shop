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


# For debugging - remove this in production
def debug_application(environ, start_response):
    """Debug application to test if Python is working"""
    status = "200 OK"
    output = b"Python is working! Django should be available."

    response_headers = [
        ("Content-type", "text/plain"),
        ("Content-Length", str(len(output))),
    ]
    start_response(status, response_headers)

    return [output]


# Use debug application for testing
application = debug_application
