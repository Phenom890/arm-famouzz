from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    SetPasswordForm,
    PasswordResetForm,
    PasswordChangeForm
)
from django.contrib.auth.models import User

from .models import Profile
from core.models import Address

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "class": "form-group"
    }))
    email = forms.EmailField()
    password1 = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput(attrs={
        "class": "form-group"
    }))
    password2 = forms.CharField(label="Confirm Password", max_length=30, widget=forms.PasswordInput(attrs={
        "class": "form-group"
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserPasswordReset(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "auto-focus": "true",
    }))


class UserPasswordResetConfirm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", max_length=30, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "auto-focus": "true",
    }))
    new_password2 = forms.CharField(label="Confirm New Password", max_length=30,
                                    widget=forms.PasswordInput(attrs={
                                        "class": "form-control",
                                        "auto-focus": "true",
                                    }))


class UserChangePassword(PasswordChangeForm):
    old_password = forms.CharField(max_length=30, label="Old Password", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "auto-focus": "true"
    }))
    new_password1 = forms.CharField(max_length=30, label="New Password", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "auto-focus": "true"
    }))
    new_password2 = forms.CharField(max_length=30, label="Confirm New Password",
                                    widget=forms.PasswordInput(attrs={
                                        "class": "form-control",
                                        "auto-focus": "true"
                                    }))


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'gender']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["locality", "street_name", "region", "house_number"]