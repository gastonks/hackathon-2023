from django import forms

class DechetForm(forms.Form):
    image = forms.ImageField()

class AjoutPointMapForm(forms.Form):
    description = forms.CharField()
    latitude = forms.DecimalField()
    longitude = forms.DecimalField()