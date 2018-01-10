from django import forms
from django.contrib.auth.models import User

class FormURL(forms.Form):
    url = forms.URLField()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm')
