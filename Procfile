release: python manage.py migrate 
release: python manage.py migrate --no-input
web: daphne quiz_site.asgi:application --port $PORT --bind 0.0.0.0