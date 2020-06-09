from django import forms
from .models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class SignUpForm(forms.ModelForm):
    # password = forms.CharField(required=True)
    check_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder': 'Again Password'}),
            required=True,
            label='비밀번호 확인'
            )

    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'email',
                  'phone_number',
                  'first_name',
                  'last_name',
                  'department',
                  'student_id'
                  ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your Phone number'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '학과'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '학번'}),
        }
        labels = {
            'username': '아이디',
            'password': '비밀번호',
            'email': '이메일',
            'phone_number': '전화번호',
            'first_name': '이름',
            'last_name': '성',
            'department':'학과',
            'student_id':'학번'
        }

    def clean_username(self):
        check_username = self.cleaned_data['username']
        if User.objects.filter(username=check_username).exists():
            raise forms.ValidationError("아이디가 이미 사용중 입니다.")
        return check_username

    def clean_email(self):
        check_email = self.cleaned_data['email']
        if User.objects.filter(email=check_email).exists():
            raise forms.ValidationError("이메일이 사용중 입니다.")
        
    def clean_check_password(self):
        password = self.cleaned_data['password']
        check_password = self.cleaned_data['check_password']
        if password =="" or check_password=="":
            raise forms.ValidationError("비밀번호를 다시 확인해주세요.")
        elif password != check_password:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return check_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


    # 폰 번호에 '-'가 2개 있어야 검증되서 통과함
    

class SignInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}),label='아이디')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Password'}),label='비밀번호')

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['time_table']

class userChangeform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'department','email', 'student_id']