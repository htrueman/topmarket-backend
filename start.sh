#!/usr/bin/env bash
echo "====== RUN MIGRATIONS ======"
python3 manage.py migrate

echo "====== COLLECT STATIC ======"
python3 manage.py collectstatic

echo "====== RUN APP ======"
gunicorn -b 0.0.0.0:8080 -w 4 top_market_platform.wsgi