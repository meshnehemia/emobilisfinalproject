from django import forms
from .models import MainBooks


class MainBooksForm(forms.ModelForm):
    class Meta:
        model = MainBooks
        fields = '__all__'
        exclude = ['auther']
