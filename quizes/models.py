from django.db import models

#figure out which models/databases are many-to-one or one-to-one etc....

class Quiz(models.Model):
    QuizType = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.QuizType


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.PROTECT,
        blank=False
    )
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class Answer(models.Model):
   question = models.ForeignKey(
       Question, 
       on_delete=models.PROTECT, 
       blank = False)
  
   answer = models.CharField(max_length=200)
   iscorrect = models.BooleanField(default=False)

   def __str__(self) -> str:
       return self.answer




'''
def answer_options(self):
        answer_options = list(Answer.objects.filter(question=self))

        empty = []

        for option in answer_options:
            empty.append({
                'answer': answer_options.answer,
                'iscorrect': answer_options.iscorrect
            })
        return empty
'''