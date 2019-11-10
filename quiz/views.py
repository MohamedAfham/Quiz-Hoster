from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Quiz

def quiz_home(request):
    if request.user.is_authenticated:
        quizzes = []
        for quiz in Quiz.objects.all():
            quizzes.append(
                {
                    'author':quiz.author,
                    'title':quiz.title,
                    'difficulty':quiz.difficulty,
                    'image':None,
                    'quiz':quiz.content,
                }
            )
        return render(request, 'quiz_home.html', {'quizzes':quizzes, 'request':request})
    else: 
        messages.warning(request, f'Login Required')
        return redirect('student-login')


def quiz_about(request):
    return render(request, 'quiz_about.html')