from django.db import models

DIFICULTIES = (
    ## value, visible choice
    ('Easy','Easy'), 
    ('Medium','Medium'), 
    ('Hard','Hard'),
)

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    ## image = models.ImageField(blank=True, null=True) add uploadto folder
    content = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFICULTIES, default='Easy')
    ## author foreigh key user : for now author is char field
    author = models.CharField(max_length=30, null=True)
