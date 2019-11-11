
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home, name='quiz-home'),
    path('page/<int:page_no>/', views.quiz_page, name='quiz-page' ),
    path('about/', views.quiz_about, name='quiz-about'),
    path('submit/', views.quiz_submit, name='quiz-submit'),
]