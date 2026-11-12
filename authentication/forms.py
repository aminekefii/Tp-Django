from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, UsernameField)

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "placeholder": "Your username"}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Your password"}))

    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": "Incorrect username or password.",
    }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        help_text="Used to recover your account.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already used.")
        return email
