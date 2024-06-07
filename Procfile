release: python manage.py migrate --no-input
web: daphne quiz_site.asgi:application --port $PORT --bind 0.0.0.0 -v2
quizworker: python manage.py runworker --settings=quiz_site.settings -v2