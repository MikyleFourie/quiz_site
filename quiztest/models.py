from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib import admin

MAX_PARTICIPANTS = 4


#category model is for future purposes when users can play a randomized quiz (it will be a bridge to pull random questions from all the quizzes)
class Category(models.Model):

    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Quizzes(models.Model):

    #all meta classes within the models are simply for better organization and readibility especially when data is viewed in the admin page. 
    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ['id']

    title = models.CharField(max_length=255, default=_(
        "New Quiz"), verbose_name=_("Quiz Title"))
    
    category = models.ForeignKey(
        Category, default=1, on_delete=models.PROTECT)#references category model, the models.PROTECT prevents deletion of the referenced object
    

    def __str__(self):
        return self.title


#the scale and type fields make use of django choices which allows the fields to have options. the choices are defined as iterables
class Question(models.Model):

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['id']

    SCALE = (
        (1, _('Beginner')), #the value on the left is the actual value in the database, the string on the right is for readability purposes 
        (2, _('Intermediate')),
        (3, _('Advanced')),

    )

    TYPE = (
        (0, _('Multiple Choice')),
        (1, _('True or False')),
        #(2, _('Text Input')), -- for future implementation
    )

    quiz = models.ForeignKey(
        Quizzes, related_name='question', on_delete=models.PROTECT)
   
    typeOfQ = models.IntegerField(
        choices=TYPE, default=0, verbose_name=_("Type of Question"), null=True)
   
    title = models.CharField(max_length=255, verbose_name=_("Title"), default ='', null=True)
   
    difficulty = models.IntegerField(
        choices=SCALE, default=0, verbose_name=_("Difficulty"), null=True)


    def __str__(self):
        return self.title


class Answer(models.Model):

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['id']

    question = models.ForeignKey(
        Question, related_name='answer', on_delete=models.PROTECT)
    

    answer_text = models.CharField(
        max_length=255, verbose_name=_("Answer Text"))
    

    is_right = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.answer_text 
    
#leaderboard model has a user and score attribute 
class Leaderboard(models.Model):
    class Meta:
        verbose_name = _("Leaderboard")
        ordering = ['score']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

   
    

class Session(models.Model):
    #Change MAX_PARTICIPANTS constant at the top to change how many players per session
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")
        ordering = ['id']


    QuizID = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    Participants = ArrayField(models.CharField(max_length=255, blank=True)) #participants and userscores are array fields (this can only be done because postgres functionality allows it, sqlite does not support arrays)
    UserScores = ArrayField(models.IntegerField(blank=True))
    QuizType = models.CharField(max_length= 255, null=True)
    QuizStatus = models.CharField(max_length= 255, null=True, default='OPEN')
    #QuizStatus should ONLY be OPEN or CLOSED

    def add_participant(self, username):
        if len(self.Participants) < MAX_PARTICIPANTS:
            self.Participants.append(username)
            self.save()
            return True
        return False
    
    def is_full(self):
        return len(self.Participants) >= MAX_PARTICIPANTS;    




#datetime for model session!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#from datetime import datetime

# Create a new session
#new_session = Session(
  #  QuizID=quiz,
   # Participants=['John', 'Jane'],
    #UserScores=[10, 15],
    #QuizType='Multiple Choice',
    #session_time=datetime.now()  # Set the session time to the current date and time

#new_session.save()


 #session_time = models.DateTimeField()

   # @property
    #def QuizType(self):
     #   return self.QuizID.title

    #session = Session.objects.get(id=1)  # get a Book instance
    #QuizType = session.author.name



