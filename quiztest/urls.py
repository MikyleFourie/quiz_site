from django.urls import path
from .views import Quiz, RandomQuestion, QuizQuestion

app_name='quiztest'

urlpatterns = [
    path('', Quiz.as_view(), name='quiztest'),
    path('r/<str:topic>/', RandomQuestion.as_view(), name='random' ),
    path('q/<str:topic>/', QuizQuestion.as_view(), name='questions' ),
]