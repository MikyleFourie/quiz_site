import random
from django import forms
from rest_framework import generics
from rest_framework.response import Response
from .models import Quizzes, Question, Answer
from .serializers import QuizSerializer, RandomQuestionSerializer, QuestionSerializer
from rest_framework.views import APIView

from django.shortcuts import render, redirect
from django.views import View
from .forms import QuizForm
#from django.http import HttpResponse, HttpResponseNotFound

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
        questions = list(quiz.question.all())

        # Check if we need to start a new quiz
        if 'question_ids' not in request.session:
            question_ids = [q.id for q in questions]
            random.shuffle(question_ids)
            request.session['question_ids'] = question_ids
            request.session['current_question_index'] = 0
            request.session['score'] = 0
        else:
            question_ids = request.session['question_ids']
            current_question_index = request.session['current_question_index']

        # Get the current question
        current_question_index = request.session['current_question_index']
        current_question_id = question_ids[current_question_index]
        current_question = Question.objects.get(id=current_question_id)

        form = QuizForm(question=current_question)
        # return render(request, 'quiz/quiz.html', {
        #     'form': form,
        #     'quiz': quiz,
        #     'question_number': current_question_index + 1,
        #     'total_questions': len(question_ids)
        # })

    def post(self, request, *args, **kwargs):
        quiz = Quizzes.objects.get(title=kwargs['title'])
        question_ids = request.session['question_ids']
        current_question_index = request.session['current_question_index']
        current_question_id = question_ids[current_question_index]
        current_question = Question.objects.get(id=current_question_id)

        form = QuizForm(request.POST, question=current_question)

        if form.is_valid():
            correct_answer = current_question.answer.filter(is_right=True).first()
            user_answer_id = form.cleaned_data[f'question_{current_question.id}']
            if str(correct_answer.id) == user_answer_id:
                request.session['score'] += 1

            # Move to the next question
            request.session['current_question_index'] += 1
            if request.session['current_question_index'] >= len(question_ids):
                score = request.session['score']
                total = len(question_ids)
                context = {
                    'score': score,
                    'total': total,
                    'quiz': quiz,
                }
                # Clear session data
                del request.session['question_ids']
                del request.session['current_question_index']
                del request.session['score']
              #  return render(request, 'quiz/result.html', context)
           # else:
              #  return redirect('quiztest:quiz', title=quiz.title)
        
        # print(form.errors)
        # return render(request, 'quiz/quiz.html', {
        #     'form': form,
        #     'quiz': quiz,
        #     'question_number': current_question_index + 1,
        #     'total_questions': len(question_ids)
        # })