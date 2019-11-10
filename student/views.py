from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

from django.contrib.auth.models import User, auth

from .models import RegisterForm
from .models import LoginForm

from django.contrib import messages
from django.db import IntegrityError

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            index = form.cleaned_data.get('index').upper()
            password = form.cleaned_data.get('password1')
            try:
                user = User.objects.create_user(index, password=password, first_name=name)
                messages.success(request, f'Account created for {name}, index : {index}, password : {password}')
                return redirect('quiz-home')
            except IntegrityError as e:
                messages.warning(request, f'Error: index already exists. (error_message={e})')
                return redirect('student-register')
        else:
            messages.warning(request, 'register form is invalid')
    else:
        form = RegisterForm()
    return render(request, 'student_register.html', {'form':form})

def login(request):
    if request.user.is_authenticated:
        return redirect('quiz-home')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                index = form.cleaned_data.get('index')
                password = form.cleaned_data.get('password')
                user = authenticate(username=index, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('quiz-home')
                else:
                    messages.warning(request, 'Authentication failed. (check your index and password)')
            else:
                messages.warning(request, 'login form is invalid')
        else:
            form  = LoginForm()
        return render(request, 'student_login.html', {'form':form} )

def logout(request):
    auth.logout(request)
    messages.success(request, 'logout success!')
    return redirect('student-login')