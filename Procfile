web: gunicorn app:app
worker: gunicorn app:app -b :8080 --timeout 10 --workers=3 --threads=3 --worker-connections=1000
