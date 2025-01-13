#!/bin/bash

set -e

while ! nc -z $DJANGO_DB_HOST $DJANGO_DB_PORT; do
  echo "Waiting for database on $DJANGO_DB_HOST:$DJANGO_DB_PORT..."
  sleep 1
done

while ! nc -z redis 6379; do
  echo "Waiting for Redis on redis:6379..."
  sleep 1
done


exec celery -A task_manager worker --loglevel=info --concurrency=1 -E -Q default