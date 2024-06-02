from django.urls import path, re_path
from . import consumers
from .consumers import QuizConsumer

websocket_urlpatterns = [
    #path(r'ws/quiz/', consumers.QuizConsumer.as_asgi()),
    #path(r'ws/quiz/<str:title>', consumers.QuizConsumer.as_asgi()),
    #path ('ws/quiz/<str:title>/', QuizConsumer.as_asgi()),
    re_path(r'ws/quiz/(?P<title>\w+)/$', QuizConsumer.as_asgi()),
]

