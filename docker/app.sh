#!/bin/bash

set -e

alembic upgrade head

gunicorn src.main:app --workers 10 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000