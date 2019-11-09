
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home, name='quiz-home'),
    path('about/', views.quiz_about, name='quiz-about'),
]