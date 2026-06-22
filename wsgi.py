from app import app as application

# Gunicorn entrypoint expects a callable named `application`
# Usage: gunicorn -w 2 -b 0.0.0.0:8082 wsgi:application















