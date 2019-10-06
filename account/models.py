from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms


# 폰 번호에 '-'가 2개 있어야 검증되서 통과함
def phone_number_validator(value):
    if value.count('-') != 2 and len(value) != 0:
        raise forms.ValidationError("'-'를 포함해주세요")
    return value


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=13, blank=True, validators=[phone_number_validator])
    time_table = models.CharField(default=('0' * 91), max_length=91)
