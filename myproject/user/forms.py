from django import forms
from django.contrib.auth.models import User


class AddUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class LogoutForm(forms.Form):
    pass
