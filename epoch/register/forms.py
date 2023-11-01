from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput


class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=TextInput(
        attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(
        attrs={'placeholder': 'Password'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(
        attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=EmailInput(
        attrs={'placeholder': 'email@gmail.com'}))
    password1 = forms.CharField(widget=PasswordInput(
        attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            return user
