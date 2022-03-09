web: gunicorn app:app --preload
worker: gunicorn --workers=9 app:app --timeout 10
