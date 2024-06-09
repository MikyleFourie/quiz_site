from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    #re_path(r'ws/quiz/(?P<title>\w+)/$', consumers.QuizConsumer.as_asgi()),
    re_path(r'ws/quiz/(?P<title>\w+)/(?P<session_id>\d+)/$', consumers.QuizConsumer.as_asgi()),
]

