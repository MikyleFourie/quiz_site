from django.contrib import admin
from .models import Quiz
from .models import Question
from .models import QuestionType
from .models import Answer

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionType)