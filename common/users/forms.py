from django import forms
from django.contrib.auth.forms import UserChangeForm
from common.users.models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email",)
