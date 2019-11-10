from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Quiz, Submission



def quiz_home(request):
    if request.user.is_authenticated:
        quizzes = []
        answers = {}
        for quiz in Quiz.objects.all():
            quizzes.append(quiz)
        
        if hasattr(request.user, 'student') :
            student = request.user.student
            for submission in Submission.objects.filter(student=student):
                answers[submission.quiz.id] = submission.answer
        return render(request, 'quiz_home.html', { 'quizzes':quizzes, 'answers':answers, 'request':request})
    else: 
        messages.warning(request, f'Login Required')
        return redirect('student-login')


def quiz_about(request):
    return render(request, 'quiz_about.html')


def quiz_submit(request):
    if not request.user.is_authenticated:
        messages.warning(request, f'Login Required')
        return redirect('student-login')

    if not hasattr(request.user, 'student') :
        messages.warning(request, f'Login Required of a Student')
        return redirect('student-login')
        
    if request.method == 'POST':
        for quiz_id in request.POST:
            if quiz_id.isdigit(): ## ignoreing csrfmiddlewaretoken
                if request.POST[quiz_id]:
                    student = request.user.student
                    quiz = Quiz.objects.get(id=int(quiz_id))
                    Submission.objects.create(student=student, quiz=quiz, answer=request.POST[quiz_id])
    messages.success(request, f'submissions success!')
    return redirect('quiz-about')
