from django import forms
from captcha.fields import CaptchaField

class CaptchaForm(forms.Form):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['captcha'].widget.attrs['captcha_key'] = 'default'
