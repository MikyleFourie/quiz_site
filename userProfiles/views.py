from re import template
from django import http
import django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm

import userProfiles
from .models import Users

# This is a single View. Sort of like a class. for now its called view1
def view1(request):
    
    myusers = Users.objects.all().values()
    template = loader.get_template('all_users.html')
    context = {
        'myusers': myusers,
        }

    return HttpResponse(template.render(context, request))

def details(request, id):
    myusers = Users.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myusers': myusers,
        }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            template = loader.get_template('quizSelection.html')
            return HttpResponse(template.render())
        
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {"form": form})

def testing(request):
  template = loader.get_template('test.html')
    
  return HttpResponse(template.render())

def qSelect(request):
    template = loader.get_template('quizSelection.html')
    return HttpResponse(template.render())