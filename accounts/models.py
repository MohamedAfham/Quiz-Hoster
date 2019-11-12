from django.db import models
from django.contrib.auth.models import User, Permission

class Student(models.Model):
    index = models.CharField(max_length=20, primary_key=True)
    student_name = models.CharField(max_length=30)
    user = models.OneToOneField( User, on_delete= models.CASCADE )

    @staticmethod
    def create_student(index, name, password):
        user = User.objects.create_user('student_'+index.upper(), password=password)
        student = Student.objects.create(index=index.upper(), student_name=name, user=user)
        return student
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super(Student, self).delete(*args, **kwargs)

    def get_username(self):
        return 'student_'+self.index

    def __str__(self):
        return self.student_name+'-'+self.index


class Staff(models.Model):
    staff_name = models.CharField(max_length=30, unique=True)
    user = models.OneToOneField( User, on_delete=models.CASCADE)

    @staticmethod
    def create_staff(name, password):
        user = User.objects.create_user(username='staff_'+name, password=password)
        user.is_staff = True
        user.user_permissions.set([
            Permission.objects.get(codename='add_quiz'),
            Permission.objects.get(codename='change_quiz'),
            Permission.objects.get(codename='delete_quiz'),
            Permission.objects.get(codename='view_quiz')
        ])
        staff = Staff.objects.create(staff_name=name, user=user)
        return staff
    
    def __str__(self):
        return self.staff_name


# Forms and Validators #################################
from django import forms

## validators
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils.deconstruct import deconstructible
@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = 0


## forms
class StudentRegisterForm(forms.Form):
    name = forms.CharField(
        max_length=150, 
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    index = forms.CharField(
        max_length=30, 
        help_text=_('Required. 30 characters or fewer. Letters will stored as Upper case'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that index already exists."),
        },
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(
                "your passwords didn't match"
            )
        return cleaned_data


class StudentLoginForm(forms.Form):
    index = forms.CharField(
        max_length=30, 
        help_text=_('Required. 30 characters or fewer. Letters must be Upper case'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that index already exists."),
        },
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )