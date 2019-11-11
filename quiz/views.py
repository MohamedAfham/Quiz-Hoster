from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from .models import Quiz, Submission

import math
QUIZ_PER_PAGE = 3


def get_progress(request):
    answer_count = 0
    if hasattr(request.user, 'student') :
            student = request.user.student
            answer_count = Submission.objects.filter(student=student).count()
    quiz_count = Quiz.objects.all().count()
    if quiz_count == 0:
        return 0
    return answer_count/quiz_count * 100


def quiz_home(request):
    return render(request, 'quiz_home.html', {'progress':get_progress(request)})
    


def quiz_page(request, page_no):
    if request.user.is_authenticated:
        
        ## create render variables
        quizzes = []
        answers = {}
        for quiz in Quiz.objects.all()[ (page_no-1)*QUIZ_PER_PAGE : (page_no-1)*QUIZ_PER_PAGE + QUIZ_PER_PAGE ]:
            quizzes.append(quiz)
        
        if hasattr(request.user, 'student') :
            student = request.user.student
            for submission in Submission.objects.filter(student=student):
                answers[submission.quiz.id] = submission.answer
        
        quiz_count = Quiz.objects.count()
        page_count = math.ceil(quiz_count/QUIZ_PER_PAGE)
        pagination = {
            'page_no' : page_no,
            'quiz_count' : quiz_count,
            'page_count' : page_count,
            'page_loop' : range(1,page_count+1),
            'previous_disabled' : (page_no == 1),
            'next_disabled' : (page_no == page_count),
            'previous_page_no' : page_no -1,
            'next_page_no' : page_no + 1,
        }
        progress = len(answers)/quiz_count * 100
        return render(request, 'quiz_page.html', { 'quizzes':quizzes, 'answers':answers, 'pagination': pagination, 'progress':progress })
    else: 
        messages.warning(request, f'Login Required')
        return redirect('student-login')


def quiz_about(request):
    return render(request, 'quiz_about.html',{ 'progress': get_progress(request) })


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

                    try:
                        submission = Submission.objects.get(quiz=quiz, student=student)
                        submission.answer = request.POST[quiz_id]
                    except Submission.DoesNotExist:
                        Submission.objects.create(student=student, quiz=quiz, answer=request.POST[quiz_id])

    next_page = int(request.POST.get('next_page'))
    if next_page == -1:
        messages.success(request, f'Quiz Submitted!')
        return redirect('quiz-about')
    else:
        return redirect('quiz-page', next_page)
