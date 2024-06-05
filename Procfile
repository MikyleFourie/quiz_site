release: python manage.py migrate --no-input
web: daphne your_project_name.asgi:application --port $PORT --bind 0.0.0.0