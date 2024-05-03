from django.urls import path
from . import views

urlpatterns = [
    path('screen1/', views.view1, name='firstScreen'),
]