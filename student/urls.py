from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='student-register'),
    path('login/', views.login, name='student-login'),
    path('logout/', views.logout, name='student-logout'),
    path('logout/conform/', views.logout_conform, name='student-logout-conform'),

]