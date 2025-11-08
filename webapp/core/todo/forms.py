from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from todo.models import User


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,required=False)
    password2 = forms.CharField(label='conf Password', widget=forms.PasswordInput,required=False)
    class Meta:
        model = User
        fields = ('username', 'chat_id')


class ChangeUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'chat_id', 'password')
