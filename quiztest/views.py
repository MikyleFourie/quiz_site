from rest_framework import generics
from rest_framework.response import Response
from .models import Quizzes, Question, Answer
from .serializers import QuizSerializer, RandomQuestionSerializer, QuestionSerializer
from rest_framework.views import APIView

from django.shortcuts import render, redirect
from django.views import View
from .forms import QuizForm

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
    
class QuizView(View):
    def get(self, request, *args, **kwargs):
        quiz = Quizzes.objects.get(title=kwargs['title'])
        questions = quiz.question.all()
        form = QuizForm(questions=questions)
        return render(request, 'quiz/quiz.html', {'form': form, 'quiz': quiz})

    def post(self, request, *args, **kwargs):
        quiz = Quizzes.objects.get(title=kwargs['title'])
        questions = quiz.question.all()
        form = QuizForm(request.POST, questions=questions)
        
        if form.is_valid():
            score = 0
            total = questions.count()
            for question in questions:
                correct_answer = question.answer.filter(is_right=True).first()
                user_answer_id = form.cleaned_data[f'question_{question.id}']
                if str(correct_answer.id) == user_answer_id:
                    score += 1
            
            context = {
                'score': score,
                'total': total,
                'quiz': quiz,
            }
            return render(request, 'quiz/result.html', context)
        
        return render(request, 'quiz/quiz.html', {'form': form, 'quiz': quiz})