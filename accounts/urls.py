from django.urls import path

from . import views

urlpatterns = [
    path('student/register/', views.student_register, name='student-register'),
    path('student/login/', views.student_login, name='student-login'),
    path('logout/', views.logout, name='account-logout'),
    path('logout/conform/', views.logout_conform, name='account-logout-conform'),
]