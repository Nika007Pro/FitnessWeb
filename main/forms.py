from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, NumberInput, FileInput

class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields =['username','email']

        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            }),
            "email": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Почта'
        })}
class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields =['name','phone_number','age', 'image']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "phone_number": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона'
            }),
            "age": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Возраст'
            })}