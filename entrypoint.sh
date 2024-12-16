#!/bin/bash

set -e

python3 manage.py migrate
exec python manage.py runserver 0.0.0.0:8000
