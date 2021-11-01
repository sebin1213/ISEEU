from django import forms
from unknown.models import record

class UnknownForm(forms.ModelForm):
    class Meta:
        model = record
        fields = '__all__'

class NicknameForm(forms.ModelForm):
    class Meta:
        model = record
        fields = ['nickname',]