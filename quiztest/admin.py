from django.contrib import admin
from . import models

@admin.register(models.Category)

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

@admin.register(models.Quizzes)

class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
    ]

class AnswerInLineModel(admin.TabularInline): #tabulare allows for two models on same page and both update
    model = models.Answer
    fields = [
        'answer_text',
        'is_right',
    ]

@admin.register(models.Question)

class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'quiz',
        'difficulty',
        'typeOfQ',
    ]
    list_display = [
        'title',
        'quiz',
        'difficulty',
        'typeOfQ',
        #'date_updated',
    ]
    inlines = [
        AnswerInLineModel,
    ]

@admin.register(models.Answer) 

class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'answer_text',
        'is_right',
        'question',
    ]