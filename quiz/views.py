from django.shortcuts import render

quizzes = [
    {
    'author':'thakee',
    'title':'Genral IQ',
    'difficulty':'E', ## E M H
    'image':None,
    'quiz': 'What\s the ...',
    },
    {
    'author':'afham',
    'title':'Country Flag',
    'difficulty':'M',
    'image':None,
    'quiz': 'What\s the ...',
    },
]


def quiz_home(request):
    return render(request, 'quiz_home.html', {'quizzes':quizzes})


def quiz_about(request):
    return render(request, 'quiz_about.html')