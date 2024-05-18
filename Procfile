release: python manage.py migrate 
web: gunicorn quiz_site.wsgi — log-file -
release: python manage.py migrate --no-input