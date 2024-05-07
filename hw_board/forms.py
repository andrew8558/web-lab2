from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import authenticate
from .models import Student


class SubmitAnswer(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

    def clean_content(self):
        data = self.cleaned_data['content']
        return data


class LoginForm(forms.Form):
    login = forms.CharField(max_length=15, label='Логин', required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8, label="Пароль")

    def clean_login(self):
        data = self.cleaned_data['login']
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        return data


class SignUpForm(forms.Form):
    name = forms.CharField(required=True, label='Имя')
    surname = forms.CharField(required=True, label='Фамилия')
    login = forms.CharField(max_length=15, label='Логин', required=True)
    email = forms.EmailField(required=True, label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8, label='Пароль')
    re_password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8, label='Повторите пароль')

    def clean_login(self):
        data = self.cleaned_data['login']
        try:
            User.objects.all().get(username=data)
            raise ValidationError('Логин занят')
        except ObjectDoesNotExist:
            return data

    def clean_password(self):
        data = self.cleaned_data['password']
        return data

    def clean_re_password(self):
        data = self.cleaned_data['re_password']
        if self.cleaned_data['password'] != self.cleaned_data['re_password']:
            raise ValidationError('Пароли не совпадают')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            Student.objects.all().get(email=data)
            raise ValidationError('Почта занята')
        except ObjectDoesNotExist:
            return data
