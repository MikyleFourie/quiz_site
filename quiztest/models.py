from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib import admin

MAX_PARTICIPANTS = 4



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
        Category, default=1, on_delete=models.PROTECT)#references category model
    

    def __str__(self):
        return self.title



class Question(models.Model):

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['id']

    SCALE = (
        (1, _('Beginner')),
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
    Participants = ArrayField(models.CharField(max_length=255, blank=True))
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







#CODE CAN BE IGNORED BELOW:

#class Updated(models.Model):

    #date_updated = models.DateTimeField(
        #verbose_name=_("Last Updated"), auto_now=True)

    #class Meta:
   #     abstract = True
    

    #date_created = models.DateTimeField(
        #auto_now_add=True, verbose_name=_("Date Created"), default='timezone.now')
    #is_active = models.BooleanField(
        #default=False, verbose_name=_("Active Status"))