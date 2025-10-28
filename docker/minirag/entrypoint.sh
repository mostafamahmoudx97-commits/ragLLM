#!/bin/bash
set -e  #if one command only fail it will stop

echo "Running database migrations..."
cd /app/models/db_schemes/minirag/
alembic upgrade head
cd /app
exec "$@"