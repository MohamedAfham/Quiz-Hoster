from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    ## image = models.ImageField(blank=True, null=True) add uploadto folder
    content = models.TextField()
    difficulty = models.CharField(max_length=1)
    ## author foreigh key user
