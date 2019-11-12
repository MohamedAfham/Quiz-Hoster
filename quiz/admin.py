from django.contrib import admin

from .models import Quiz, Submission, Variable, Feedback

admin.site.register(Quiz)
admin.site.register(Submission)
admin.site.register(Variable)
admin.site.register(Feedback)