from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm
)
from .models import CustomUser, CreatedSite


class RegistrationForm(UserCreationForm):
    """
    Form for user registration.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1']


class LoginForm(AuthenticationForm):
    """
    Form for user login.
    """

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class CustomUserCreationForm(UserCreationForm):
    """
    Extended form for user creation with additional password validation.
    """
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password1']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1


class UserEditForm(UserChangeForm):
    """
    Form for editing user profile information.
    """

    class Meta:
        model = CustomUser
        fields = ['email', 'username']


class CreateSiteForm(forms.ModelForm):
    """
    Form for creating a new site.
    """

    class Meta:
        model = CreatedSite
        fields = ['name', 'url']
