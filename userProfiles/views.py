from re import template
from django import http
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

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

def testing(request):
  myUsersList = Users.objects.all().values()
  template = loader.get_template('template.html')
  #context = {
   #   'myUsers': myUsersList,
   #   }
  context = {
      'fruits': ['Apple', 'Cherry', 'Grapes']
      }
  
  return HttpResponse(template.render(context, request))

