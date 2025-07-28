#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create staticfiles directory
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate