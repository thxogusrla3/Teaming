from django import forms
from account.models import User
from .models import Mail

class MailForm(forms.ModelForm):
    username = forms.CharField(max_length=20)
    class Meta:
        model = Mail
        fields = ['username', 'content']
