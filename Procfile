release: python manage.py migrate 
web: gunicorn quiz_site.wsgi — log-file -
release: manage.py migrate --no-input