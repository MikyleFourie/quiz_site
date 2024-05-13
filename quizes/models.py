from django.db import models

#figure out which models/databases are many-to-one or one-to-one etc....

class Quiz(models.Model):
    QuizType = models.CharField(max_length=50)

class Question(models.Model):
    QuestionType= models.IntegerField()
    quiztype = models.ForeignKey(Quiz)
    question = models.CharField(max_length=200)
    #use choices??

    
class Answer(models.Model):
    answer = models.TextChoices
    #use choices??

class AnswersToQuestion(models.Model):
    answer = models.ForeignKey(Answer)
    question = models.ForeignKey(Question)

class Response(models.Model):
    #updated real time with each response 
    quiz_id = models.ForeignKey(Quiz)
    question_id = models.ForeignKey(Question)
    response = models.CharField(max_length=100) #how to check if response matches answer to question set....
    isCorrect = models.BooleanField() #depends on if response answer matches the correct answer


#put the following classes in user app

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    #password field...hashfunction stuff goes here...
    games_played = models.IntegerField(null=True)

class GameSessions(models.Model):
    user_id = models.ForeignKey(User)
    quiz_id = models.ForeignKey(Quiz)
    date_time = models.DateTimeField()
    score = models.IntegerField(null=True)
    totalTime = models.TimeField()


#put following classes in Admin app

