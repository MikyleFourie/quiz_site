from django.contrib import admin
from . import models



@admin.register(models.Category)

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'id',
    ]

    search_fields = ['id', 'name']
    
    list_filter = ['name']
   



@admin.register(models.Quizzes)

class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
    ]

    search_fields = ['id', 'title']
    
    list_filter = ['title']

class AnswerInLineModel(admin.TabularInline): #tabulare allows for two models on same page and both update
    model = models.Answer
    fields = [
        'id',
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

    search_fields = ['id', 'title', 'quiz', 'difficulty']
    
    list_filter = ['quiz', 'typeOfQ', 'difficulty']

@admin.register(models.Answer) 

class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'answer_text',
        'is_right',
        'question',
    ]

    search_fields = ['id', 'answer_text', 'is_right', 'question']
    
    list_filter = ['question', 'is_right']

@admin.register(models.Leaderboard) 

class LeaderboardAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'score',
       
    ]

    list_filter = ['user', 'score']

@admin.register(models.Session) 

class SessionAdmin(admin.ModelAdmin):
    list_display = [
        'QuizID',
        'Participants',
        'UserScores',
        'QuizType',
    ]

    list_filter = ['QuizID', 'QuizType', 'Participants']