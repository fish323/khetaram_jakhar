from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmailSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. A valid email address to receive OTP.')

    class Meta:
        model = User
        fields = ('username', 'email')