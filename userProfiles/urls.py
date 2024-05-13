from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('allUsers/', views.view1, name='firstScreen'),
    path('allUsers/details/<int:id>', views.details, name='detailsScreen'),
    path('testing/', views.testing, name='testing'),    
    path('login/', views.login, name='login'),
    path('register/', views.register, name="register"),
    path('qSelect/', views.qSelect, name='quizSelect'),
]