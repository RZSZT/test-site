from django import forms

class GifForm(forms.ModelForm):
   picture = forms.ImageField()
