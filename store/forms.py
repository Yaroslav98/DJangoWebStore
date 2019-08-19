from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserInfo

class UserForm(UserCreationForm):
    email = forms.EmailField(label='Email',required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserInfoForm(forms.ModelForm):
    class Meta:
        model=UserInfo
        fields=("info","phonenumber","photo")