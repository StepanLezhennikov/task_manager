#!/bin/bash

set -e

exec celery -A task_manager worker --loglevel=info --concurrency=1 -E -Q default