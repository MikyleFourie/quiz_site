from django.urls import path
from .views import Quiz, RandomQuestion, QuizQuestion, QuizView

app_name='quiztest'

urlpatterns = [
    #path('', Quiz.as_view(), name='quiztest'),
    path('r/<str:topic>/', RandomQuestion.as_view(), name='random' ),
    path('q/<str:topic>/', QuizQuestion.as_view(), name='questions' ),

    path('', QuizView.as_view(), name='quiztest'),
    path('<str:title>/', QuizView.as_view(), name='quiz'),
    #path('<str:title>/', QuizView.as_view(), name='result.html'),
]