from django import forms

class FormURL(forms.Form):
    url = forms.URLField()
