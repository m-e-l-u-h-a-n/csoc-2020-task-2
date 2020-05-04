from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    firstname = forms.CharField(max_length=24,help_text='Optional', required=False)
    lastname = forms.CharField(max_length=24,help_text='Optional', required=False)
    email=forms.EmailField(max_length=200, required=True,help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = ('firstname', 'lastname','username', 'email', 'password1', 'password2')