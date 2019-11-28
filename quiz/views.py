from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from .models import Quiz, Submission, Variable
from accounts.models import Student

import math
QUIZ_PER_PAGE = 5

def get_result_progress(request):
    submissions = Submission.objects.none()
    if hasattr(request.user, 'student'):
        student = request.user.student
        submissions = Submission.objects.filter(student=student)
    else:
        return dict()
    quiz_count = Quiz.objects.all().count()
    correct_answers = 0
    wrong_answers = 0
    for sub in submissions:
        if sub.answer == sub.quiz.correct_answer: correct_answers += 1
        else: wrong_answers += 1
    correct = int(correct_answers/quiz_count * 100)
    wrong   = int( wrong_answers/quiz_count * 100 )
    empty   = 100 - ( correct + wrong )
    return {'result_success': correct, 'result_empty':empty, 'result_failed':wrong, 'correct_answers':correct_answers, 'quiz_count':quiz_count}
    

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
    var, created = Variable.objects.get_or_create(id=1)
    ctx = {'progress':get_progress(request), 'quiz_ended':var.quiz_end}
    ctx.update(get_result_progress(request))
    return render(request, 'quiz_home.html', ctx )
    
    


def quiz_page(request, page_no):
    if request.user.is_authenticated:
        ## check quiz ended
        var, created = Variable.objects.get_or_create(id=1)
        if var.quiz_end:
            messages.warning(request, f'Quiz ended, can\'t  attempt anymore.')
            return redirect('quiz-about') ## TODO:

        ## create render variables
        quizzes = []
        answers = dict()
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

        ## not a good code
        progress = 0
        if quiz_count != 0:
            progress = len(answers)/quiz_count * 100
        ctx = {
            'quizzes':quizzes, 'answers':answers, 'pagination': pagination, 'progress':progress, 
            'quiz_ended': Variable.objects.get(id=1).quiz_end
        }
        ctx.update(get_result_progress(request))
        return render(request, 'quiz_page.html', ctx )
    else: 
        messages.warning(request, f'Login Required')
        return redirect('student-login')


def quiz_about(request):
    ctx = { 'progress': get_progress(request), 'quiz_ended':Variable.objects.get(id=1).quiz_end }
    ctx.update(get_result_progress(request))
    return render(request, 'quiz_about.html', ctx)


def quiz_submit(request):
     ## check quiz ended
    var, created = Variable.objects.get_or_create(id=1)
    if var.quiz_end:
        messages.warning(request, f'Quiz ended, can\'t  attempt anymore.')
        return redirect('quiz-about') ## TODO:

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
                        submission.answer = int(request.POST[quiz_id])
                        submission.save()
                    except Submission.DoesNotExist:
                        Submission.objects.create(student=student, quiz=quiz, answer=request.POST[quiz_id])

    next_page = int(request.POST.get('next_page'))
    if next_page == -1 or not next_page:
        messages.success(request, f'Quiz Submitted!')
        return redirect('quiz-about')
    else:
        return redirect('quiz-page', next_page)

###############################################################################

def quiz_view_result(request, page_no):
    if request.user.is_authenticated:

        ## check quiz ended
        var, created = Variable.objects.get_or_create(id=1)
        if hasattr(request.user, 'student'):
            if not var.quiz_end:
                messages.warning(request, f'This will be available once the quiz ended.')
                return redirect('quiz-page', 1)

        ## create render variables
        quizzes = []
        answers = dict()
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

        ## view radio colors
        color_table = []
        for quiz in quizzes:
            if quiz.id in answers.keys():
                if answers[quiz.id] == quiz.correct_answer:
                    for i in range(1,5):
                        if i == quiz.correct_answer: color_table.append( (quiz.id, i, 'green') )
                        else: color_table.append( (quiz.id, i, 'none') )
                else:
                    for i in range(1,5):
                        if i == quiz.correct_answer: color_table.append( (quiz.id, i, 'yellow') )
                        elif i == answers[quiz.id] : color_table.append( (quiz.id, i, 'red') )
                        else: color_table.append( (quiz.id, i, 'none') )
            else:
                for i in range(1,5):
                    if i == quiz.correct_answer  : color_table.append( (quiz.id, i, 'yellow') )
                    else: color_table.append( (quiz.id, i, 'none') )

        

        ## not a good code
        progress = 0
        if quiz_count != 0:
            progress = len(answers)/quiz_count * 100

        ctx = { 
            'quizzes':quizzes,  'color_table':color_table, 'answers':answers, 'pagination': pagination, 'progress':progress,
            'view_result_active' : 'active', 'quiz_ended': Variable.objects.get(id=1).quiz_end
        }
        ctx.update(get_result_progress(request))
        return render(request, 'quiz_view_result.html', ctx)
    else: 
        messages.warning(request, f'Login Required')
        return redirect('student-login')


from .leaderboard import get_leaderboard
def quiz_leaderboard(request):
    if request.user.is_authenticated:
        ## check quiz ended
        if not request.user.is_staff:
            var, created = Variable.objects.get_or_create(id=1)
            if hasattr(request.user, 'student'):
                if not var.quiz_end:
                    messages.warning(request, f'This will be available once the quiz ended.')
                    return redirect('quiz-page', 1)

        lboard = get_leaderboard(Quiz, Student, Submission)
        lboard.sort( key = lambda tup:tup[1], reverse=True )
        lboard = list(map(lambda pair: [pair[0],'%.2f'%pair[1]],lboard))
        for i in range(len(lboard)):
            lboard[i].append(i+1)
        ctx = { 
            'leaderboard_active':'active', 'quiz_ended': Variable.objects.get(id=1).quiz_end,
            'lboard': lboard  ## TODO: order them
        }
        ctx.update(get_result_progress(request))
        return render(request, 'quiz_leaderboard.html',  ctx )
    else: 
        messages.warning(request, f'Login Required')
        return redirect('student-login')

from .models import FeedbackForm, Feedback
def quiz_feedback(request):
    if request.user.is_authenticated:
        ## check quiz ended
        var, created = Variable.objects.get_or_create(id=1)
        if not var.quiz_end:
            messages.warning(request, f'This will be available once the quiz ended.')
            return redirect('quiz-page', 1)

        ## check if student
        if not hasattr(request.user, 'student') :
            messages.warning(request, f'Login Required of a Student')
            return redirect('quiz-about') ## TODO:

        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
               feedback = form.cleaned_data.get('feedback')
               Feedback.objects.create(student=request.user.student, feedback=feedback)
               messages.success(request, f'Feedback sent successfully!')
               return redirect('quiz-about') ## TODO:
        else:
            form = FeedbackForm()
        
        ctx = { 'form': form, 'feedback_active':'active','quiz_ended': Variable.objects.get(id=1).quiz_end, }
        ctx.update(get_result_progress(request))
        return render(request, 'quiz_feedback.html', ctx )

    else: 
        messages.warning(request, f'Login Required')
        return redirect('student-login')
