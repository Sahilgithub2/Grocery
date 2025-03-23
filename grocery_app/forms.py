from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField  # ✅ Import CAPTCHA

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()  # ✅ Ensure CAPTCHA is included
