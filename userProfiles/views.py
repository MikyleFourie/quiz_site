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
from django.db.models import Max
from django.conf import settings
from django.shortcuts import redirect
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
    #This blocks access to quizes by unauthenticated users
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    template = loader.get_template('userProfiles/quizSelection.html')
    return HttpResponse(template.render())

def quiz(request, title, session_id):
    quiz = get_object_or_404(Quizzes, title=title)
    # Try to get the session with the provided session_id
    session = get_object_or_404(Session, id=session_id)

    # If session doesn't exist, create a new one
    if not session:
        session = Session.objects.create(QuizID=quiz, QuizType=title, Participants=[], UserScores=[])

    # Add current user to the session
    if session.add_participant(request.user.username):
        #request.session['session_id'] = session.id
        question_ids = random.sample([q.id for q in quiz.question.all()], 10)
        request.session['question_ids'] = question_ids

        context = {
            'quiz_title': title,
            'session_id': session_id
        }
    else:
        return redirect('quizSelect')

    return render(request, 'userProfiles/quiz.html', context)

    # #Try find first available session
    # session = Session.objects.filter(QuizID=quiz, QuizType=title).exclude(Participants__len=MAX_PARTICIPANTS).first()
    # if not session:
    #     #Create a new session if no others are available
    #     session = Session.objects.create(QuizID=quiz, QuizType=title, Participants=[], UserScores=[])

    # #Add current user to the session
    # if session.add_participant(request.user.username):
    #     request.session['session_id'] = session.id
    #     question_ids = random.sample([q.id for q in quiz.question.all()], 10)
    #     request.session['question_ids'] = question_ids

    #     context = {
    #         'quiz_title': title,
    #         'session_id': session.id
    #     }
    # else:
    #     return redirect('quizSelect') #not sure if this line works
    
    # return render(request, 'userProfiles/quiz.html', context)


def leaderboard(request):

    # Get the highest score for each user
    highest_scores = Leaderboard.objects.values('user__username').annotate(max_score=Max('score'))
   

    # Now `highest_scores` contains a queryset with each user's highest score
    #A list called leaderboard is created to store the username and corresponding high score
    leaderboard = []
    # For Loop iterates through it to access user IDs and their corresponding highest scores
    for entry in highest_scores:
        user= entry['user__username']
        highest_score = entry['max_score']
        leaderboard.append({'username': user, 'highest_score': highest_score})#list is appended

    #the list is sorted after the iteration so that most recent entry is accounted for. User with the highest score overall sits at the top 
    leaderboard.sort(key=lambda entry: entry['highest_score'], reverse=True)
    # Pass the leaderboard list to the template
    context = {
        'leaderboard':leaderboard
        }

    # Render the template with the context
    return render(request, 'userProfiles/leaderboard.html', context)

def available_sessions(request, quiz_type):
    quiz = get_object_or_404(Quizzes, title=quiz_type)
    # Retrieve available sessions for the selected quiz type
    available_sessions = Session.objects.filter(QuizType=quiz_type)
    
    all_closed = all(session.QuizStatus == 'CLOSED' for session in available_sessions)
    if all_closed:
        new_session = Session.objects.create(QuizID=quiz, QuizType=quiz_type, Participants=[], UserScores=[])
        next_session_id = new_session.id
    else:
        next_session_id = available_sessions.last().id + 1 if available_sessions.exists() else 1



    # Prepare context to pass to the template
    context = {
        'quiz_type': quiz_type,
        'available_sessions': available_sessions,
        'all_closed': all_closed,
        'next_session_id': next_session_id,
    }

    return render(request, 'userProfiles/available_sessions.html', context)
