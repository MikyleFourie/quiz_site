from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from quizes.models import Quiz

#tables for users

#manually creating a game session table...look into integrating django-sessions
class GameSession(models.Model):
    user= models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=False) #sort out this user thing.....
    
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.PROTECT,
        blank=False  )
    
    date_time = models.DateTimeField()

    score = models.IntegerField(null=True)

    totalTime = models.TimeField()

    

    
