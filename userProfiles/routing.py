from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/quiz/', consumers.QuizConsumer.as_asgi()),
]

