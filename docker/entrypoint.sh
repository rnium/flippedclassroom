#!/bin/sh
set -e

python - <<'PY'
import os, sys, time
import psycopg2

for _ in range(60):
    try:
        psycopg2.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ.get("POSTGRES_HOST", "db"),
            port=os.environ.get("POSTGRES_PORT", "5432"),
        ).close()
        break
    except psycopg2.OperationalError:
        time.sleep(1)
else:
    sys.exit("postgres unreachable")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

exec "$@"
