from django.shortcuts import render, redirect

from .models import StudentForm
from django.contrib.auth.models import User
from .models import Student
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            index = form.cleaned_data.get('index')
            password = form.cleaned_data.get('password1')
            ##user = User.objects.create_user(index, password=password, first_name=name)
            messages.success(request, f'Account created for {name}, index : {index}, password : {password}')
            return redirect('quiz-home')
    else:
        form = StudentForm()
    return render(request, 'student_register.html', {'form':form})
