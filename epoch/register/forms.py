from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from .models import UserConfig, EmailSettings, TextSettings, ExportSettings


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


class UserConfigForm(forms.ModelForm):
    class Meta:
        model = UserConfig
        fields = ["timezone"]


class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(EmailSettingsForm, self).__init__(*args, **kwargs)
        self.fields['is_email_notifications_active'].label = 'Email Notifications'


class TextSettingsForm(forms.ModelForm):
    class Meta:
        model = TextSettings
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(TextSettingsForm, self).__init__(*args, **kwargs)
        self.fields['is_text_notifications_active'].label = 'Text Notifications'


class ExportSettingsForm(forms.ModelForm):
    class Meta:
        model = ExportSettings
        fields = "__all__"
