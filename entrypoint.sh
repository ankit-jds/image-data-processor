#!/bin/sh
if [ "$RUN_CELERY" = "true" ]; then
    celery -A image_processor worker --loglevel=info
else
    gunicorn --bind 0.0.0.0:8000 image_processor.wsgi:application
fi
