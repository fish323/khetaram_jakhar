from django import forms
from .models import Feedback

class Feedform(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name','email','mobile_no','district','massage']

