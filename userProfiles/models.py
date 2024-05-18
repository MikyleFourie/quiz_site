from django.db import models

class Users(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)
    

#For test implementation
class Quiz(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    quiz_type = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    
    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

