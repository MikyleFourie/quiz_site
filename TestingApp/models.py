from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions import base_session
from quizes.models import Quiz

#tables for users

#manually creating a game session table...look into integrating django-sessions
class GameSession(models.Model):
    user= models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=False) #sort out this user thing.....ok update...it's kinda working
    
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.PROTECT,
        blank=False  ) #this is working
    
    datetime = models.DateTimeField() #get datetime from django-sessions.......

    score = models.IntegerField(null=True) #must pull from score function

    totalTime = models.TimeField()#must pull from time function

    

    
