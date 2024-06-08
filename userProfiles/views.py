from re import template
import random
from django import http
import django
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.socialaccount.forms import SignupForm
from django.views import View


import userProfiles
from quiztest.models import *
from quiztest.forms import QuizForm

# This is a single View. Sort of like a class. for now its called view1
def view1(request):
    
    myusers = Users.objects.all().values()
    template = loader.get_template('userProfiles/all_users.html')
    context = {
        'myusers': myusers,
        }

    return HttpResponse(template.render(context, request))

def details(request, id):
    myusers = Users.objects.get(id=id)
    template = loader.get_template('userProfiles/details.html')
    context = {
        'myusers': myusers,
        }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('userProfiles/main.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('userProfiles/login.html')
    return HttpResponse(template.render())

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            template = loader.get_template('userProfiles/quizSelection.html')
            return HttpResponse(template.render())
        
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {"form": form})

def register2(request):
    template = loader.get_template('accounts/signup.html')
    return HttpResponse(template.render())

def testing(request):
    template = loader.get_template('userProfiles/test.html')
    return HttpResponse(template.render())

def qSelect(request):
    template = loader.get_template('userProfiles/quizSelection.html')
    return HttpResponse(template.render())

def quiz(request, title):
    quiz = get_object_or_404(Quizzes, title=title)

    #Try find first available session
    session = Session.objects.filter(QuizID=quiz, QuizType=title).exclude(Participants__len=MAX_PARTICIPANTS).first()
    if not session:
        #Create a new session if no others are available
        session = Session.objects.create(QuizID=quiz, QuizType=title, Participants=[], UserScores=[])

    #Add current user to the session
    if session.add_participant(request.user.username):
        request.session['session_id'] = session.id
        question_ids = random.sample([q.id for q in quiz.question.all()], 10)
        request.session['question_ids'] = question_ids

        context = {
            'quiz_title': title,
            'session_id': session.id
        }
    else:
        return redirect('quizSelect') #not sure if this line works
    
    return render(request, 'userProfiles/quiz.html', context)


    # quiz = Quizzes.objects.get(title=title)
    # questions = list(quiz.question.all())
    # question_ids = random.sample([q.id for q in questions], 10)

    # request.session['question_ids'] = question_ids
    
    # context = {
    #     'quiz_title': title,
    # }
    
    # return render(request, 'userProfiles/quiz.html', context)

def leaderboard(request):
    
    leaderboard = Leaderboard.objects.all()
    
    # Pass the leaderboard data to the template
    context = {'leaderboard': leaderboard}

    # Render the template with the context
    return render(request, 'userProfiles/leaderboard.html', context)





#class QuizView(View):
    # def get(self, request, *args, **kwargs):
    #     quiz = Quizzes.objects.get(title=kwargs['title'])
    #     questions = list(quiz.question.all())

    #     # Check if we need to start a new quiz
    #     if 'question_ids' not in request.session:
    #         question_ids = [q.id for q in questions]
    #         random.shuffle(question_ids)
    #         request.session['question_ids'] = question_ids
    #         request.session['current_question_index'] = 0
    #         request.session['score'] = 0
    #     else:
    #         question_ids = request.session['question_ids']
    #         current_question_index = request.session['current_question_index']

    #     # Get the current question
    #     current_question_index = request.session['current_question_index']
    #     current_question_id = question_ids[current_question_index]
    #     current_question = Question.objects.get(id=current_question_id)

    #     form = QuizForm(question=current_question)
        # return render(request, 'quiz/quiz.html', {
        #     'form': form,
        #     'quiz': quiz,
        #     'question_number': current_question_index + 1,
        #     'total_questions': len(question_ids)
        # })

    # def post(self, request, *args, **kwargs):
    #     quiz = Quizzes.objects.get(title=kwargs['title'])
    #     question_ids = request.session['question_ids']
    #     current_question_index = request.session['current_question_index']
    #     current_question_id = question_ids[current_question_index]
    #     current_question = Question.objects.get(id=current_question_id)

    #     form = QuizForm(request.POST, question=current_question)

    #     if form.is_valid():
    #         correct_answer = current_question.answer.filter(is_right=True).first()
    #         user_answer_id = form.cleaned_data[f'question_{current_question.id}']
    #         if str(correct_answer.id) == user_answer_id:
    #             request.session['score'] += 1

    #         # Move to the next question
    #         request.session['current_question_index'] += 1
    #         if request.session['current_question_index'] >= len(question_ids):
    #             score = request.session['score']
    #             total = len(question_ids)
    #             context = {
    #                 'score': score,
    #                 'total': total,
    #                 'quiz': quiz,
    #             }
    #             # Clear session data
    #             del request.session['question_ids']
    #             del request.session['current_question_index']
    #             del request.session['score']
        #         return render(request, 'quiz/result.html', context)
        #     else:
        #         return redirect('quiztest:quiz', title=quiz.title)
        
        # print(form.errors)
        # return render(request, 'quiz/quiz.html', {
        #     'form': form,
        #     'quiz': quiz,
        #     'question_number': current_question_index + 1,
        #     'total_questions': len(question_ids)
        # })
    
    