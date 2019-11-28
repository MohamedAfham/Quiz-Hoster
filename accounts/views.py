from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

from django.contrib.auth.models import User, auth

from .models import Student, Staff
from .models import StudentRegisterForm, StudentLoginForm

from django.contrib import messages
from django.db import IntegrityError

def student_register(request):
    if not request.user.is_staff:
        messages.warning(request, "you don't have access to the register page")
        return redirect('student-login')
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            index = form.cleaned_data.get('index').upper()
            password = form.cleaned_data.get('password1')
            try:
                student = Student.create_student(index, name, password)
                messages.success(request, f'Account created for {name}, index : {index}')
                ##auth.login(request, student.user)
                return redirect('student-register')
            except IntegrityError as e:
                messages.warning(request, f'Error: index already exists. (error_message={e})')
                return redirect('student-register')
        else:
            messages.warning(request, 'register form is invalid')
    else:
        form = StudentRegisterForm()
    return render(request, 'student_register.html', {'form':form})

def student_login(request):
    if request.user.is_authenticated:
        return redirect('quiz-home')
    else:
        if request.method == 'POST':
            form = StudentLoginForm(request.POST)
            if form.is_valid():
                index = form.cleaned_data.get('index').upper()
                password = form.cleaned_data.get('password')
                if Student.objects.filter(index=index).exists():
                    student = Student.objects.get(index=index)
                    user = authenticate(username=student.get_username(), password=password)
                    if user is not None:
                        auth.login(request, user)
                        messages.success(request, 'logged in successfully!')
                        return redirect('quiz-home')
                else:
                    messages.warning(request, 'Authentication failed. (check your index and password)')
            else:
                messages.warning(request, 'login form is invalid')
        else:
            form  = StudentLoginForm()
        return render(request, 'student_login.html', {'form':form} )

from quiz.views import get_progress, get_result_progress
from quiz.models import Variable
def logout(request):
    ctx = {'progress':get_progress(request),  'quiz_ended': Variable.objects.get(id=1).quiz_end, }
    ctx.update(get_result_progress(request))
    return render(request, 'account_logout.html', ctx)

def logout_conform(request):
    yes = request.GET.get('yes')
    if yes is not None:
        auth.logout(request)
        messages.success(request, f'logout success!')
        return redirect('student-login')
    else:
        return redirect('quiz-home')
