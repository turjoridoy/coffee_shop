#!/usr/bin/env python3
"""
Test WSGI file to verify Django application
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ["DJANGO_SETTINGS_MODULE"] = "conf.settings"

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application


def application(environ, start_response):
    """Simple test application"""
    status = "200 OK"
    output = b"Django application is working!"

    response_headers = [
        ("Content-type", "text/plain"),
        ("Content-Length", str(len(output))),
    ]
    start_response(status, response_headers)

    return [output]
