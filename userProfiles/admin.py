from django.contrib import admin
from .models import *

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "joined_date")
    

admin.site.register(Users, UsersAdmin)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
