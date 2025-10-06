#!/usr/bin/env bash
set -euo pipefail

python -c "import os; print('DEBUG=', os.environ.get('DEBUG'))"

# Migrate DB
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create log dir if missing
mkdir -p logs

# Run Django with Daphne (ASGI) to support Channels if used
if [ "${USE_DAPHNE:-1}" = "1" ]; then
  exec daphne -b 0.0.0.0 -p 8000 config.asgi:application
else
  exec python manage.py runserver 0.0.0.0:8000
fi


