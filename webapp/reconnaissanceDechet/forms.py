from django import forms

class DechetForm(forms.Form):
    image = forms.ImageField()