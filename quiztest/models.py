from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Quizzes(models.Model):

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ['id']

    title = models.CharField(max_length=255, default=_(
        "New Quiz"), verbose_name=_("Quiz Title"))
    
    category = models.ForeignKey(
        Category, default=1, on_delete=models.PROTECT)
    #date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Updated(models.Model):

    #date_updated = models.DateTimeField(
        #verbose_name=_("Last Updated"), auto_now=True)

    class Meta:
        abstract = True


class Question(Updated):

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
        #(2, _('Text Input')),
    )

    quiz = models.ForeignKey(
        Quizzes, related_name='question', on_delete=models.PROTECT)
   
    typeOfQ = models.IntegerField(
        choices=TYPE, default=0, verbose_name=_("Type of Question"))
   
    title = models.CharField(max_length=255, verbose_name=_("Title"), default ='', null=True)
   
    difficulty = models.IntegerField(
        choices=SCALE, default=0, verbose_name=_("Difficulty"), null=True)
    

    #date_created = models.DateTimeField(
        #auto_now_add=True, verbose_name=_("Date Created"), default='timezone.now')
    #is_active = models.BooleanField(
        #default=False, verbose_name=_("Active Status"))

    def __str__(self):
        return self.title


class Answer(Updated):

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
        return self.answer_text #this needs to return a string variable