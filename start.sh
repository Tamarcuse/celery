#!/bin/sh
celery -A tasks worker --loglevel=INFO &
celery -A tasks beat --loglevel=INFO