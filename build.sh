 #!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files for Django Admin and other static assets
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate