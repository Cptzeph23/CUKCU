#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate --noinput

# Create robots.txt for SEO
mkdir -p staticfiles
echo "User-agent: *" > staticfiles/robots.txt
echo "Allow: /" >> staticfiles/robots.txt
echo "Sitemap: https://cukcu.org/sitemap.xml" >> staticfiles/robots.txt