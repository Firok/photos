#!/bin/bash

python /docker/django/wait_for_postgres.py

# should be called from photos/ folder as there are relative paths
cd /app/
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8000
