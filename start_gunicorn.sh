#!/bin/bash

# Coffee Shop Manager - Gunicorn Startup Script

# Set the project directory
PROJECT_DIR="/home/u183730229/domains/ludwigpfeiffer.com.bd/public_html/coffee_shop"
cd $PROJECT_DIR

# Activate virtual environment
source env/bin/activate

# Set environment variables
export DJANGO_SETTINGS_MODULE=conf.settings
export PYTHONPATH=$PROJECT_DIR

# Create log and tmp directories if they don't exist
mkdir -p /home/u183730229/logs
mkdir -p /home/u183730229/tmp

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn \
    --config gunicorn.conf.py \
    --bind 127.0.0.1:8000 \
    --workers 3 \
    --timeout 30 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile /home/u183730229/logs/gunicorn_access.log \
    --error-logfile /home/u183730229/logs/gunicorn_error.log \
    --log-level info \
    --preload \
    conf.wsgi:application