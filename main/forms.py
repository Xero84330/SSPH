from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'isauthor', 'country', 'password1', 'password2')

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'isauthor', 'country')
