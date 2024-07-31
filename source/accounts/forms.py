from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from accounts.models import Profile


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}


def file_size(value):  # add this to some file where you can import it from
    limit = 300
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')


class ProfileChangeForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, validators=[
        FileExtensionValidator(['png'], "Можно загружать только png файлы"),
        file_size
    ])

    class Meta:
        model = Profile
        fields = ['birth_date', "avatar"]
