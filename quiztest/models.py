from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

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
    
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")
        ordering = ['id']


    QuizID = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    
    Participants = ArrayField(models.CharField(max_length=255, blank=True))
    UserScores = ArrayField(models.IntegerField(blank=True))

    QuizType = models.CharField(max_length= 255, null=True)


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

