from django.db import models

DIFICULTIES = (
    ## value, visible choice
    ('Easy','Easy'), 
    ('Medium','Medium'), 
    ('Hard','Hard'),
)

CORRECT_ANSWER = (
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
)

from accounts.models import Staff, Student

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    difficulty = models.CharField(max_length=10, choices=DIFICULTIES, default='Easy')
    author = models.ForeignKey(Staff, on_delete=models.CASCADE)
    content = models.TextField(default="")
    answer1 = models.CharField(max_length=30, default="")
    answer2 = models.CharField(max_length=30, default="")
    answer3 = models.CharField(max_length=30, default="")
    answer4 = models.CharField(max_length=30, default="")
    correct_answer = models.IntegerField(choices=CORRECT_ANSWER, default=1)

    def __str__(self):
        return str(self.id)+'. '+self.title

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer = models.IntegerField()

    def __str__(self):
        return f'q{self.quiz.id}-{self.student.index}'
