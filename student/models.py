from django.db import models

from django.contrib.auth.forms import UserCreationForm

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
class RegisterForm(forms.Form):
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


class LoginForm(forms.Form):
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