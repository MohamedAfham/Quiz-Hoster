from django.db import models

from django.contrib.auth.models import User 

class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    index = models.CharField(max_length=20)