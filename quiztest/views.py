from rest_framework import generics
from rest_framework.response import Response
from .models import Quizzes, Question
from .serializers import QuizSerializer, RandomQuestionSerializer, QuestionSerializer
from rest_framework.views import APIView

class Quiz(generics.ListAPIView):

    serializer_class = QuizSerializer
    queryset = Quizzes.objects.all()

class RandomQuestion(APIView):

    def get(self, request, format=None, **kwargs): #keyword arguments
        question = Question.objects.filter(quiz__title=kwargs['topic']).order_by('?')[:1] #gets question based on the quiz title and randomises order
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)

class QuizQuestion(APIView):

    def get(self, request, format=None, **kwargs):
        quiztest = Question.objects.filter(quiz__title=kwargs['topic'])
        serializer = QuestionSerializer(quiztest, many=True)
        return Response(serializer.data)