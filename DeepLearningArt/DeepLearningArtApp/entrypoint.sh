#!/bin/sh
set -x

# Collect the static files
echo Collecting static files.
python manage.py collectstatic --no-input

exec "$@"