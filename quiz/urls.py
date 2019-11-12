
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home, name='quiz-home'),
    path('page/<int:page_no>/', views.quiz_page, name='quiz-page' ),
    path('about/', views.quiz_about, name='quiz-about'),
    path('submit/', views.quiz_submit, name='quiz-submit'),

    ## after quiz end
    path('view_result/<int:page_no>/', views.quiz_view_result, name='quiz-view_result'),
    path('leaderboard/', views.quiz_leaderboard, name='quiz-leaderboard'),
    path('feedback/', views.quiz_feedback, name='quiz-feedback'),
]