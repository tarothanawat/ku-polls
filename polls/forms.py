"""Forms for user signup."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Form for user signup."""

    email = forms.EmailField(required=True)

    class Meta:
        """Class for storing signup form."""

        model = User
        fields = ('username', 'email', 'password1', 'password2')
