from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, AuthenticationForm


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ForgotPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)


class PasswordResetForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text="Required. Provide a valid email address.", required=True, error_messages={
        'required': 'Provide the email.',
        'invalid': 'Provide a valid email.',
        'unique': 'Username with such email already exists!'
    })
    nickname = forms.CharField(max_length=50, help_text="Optional. Provide a nickname for your account.", required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'nickname', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        return super().save(commit)


class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(label='Upload a new photo:', widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['profile_picture', 'desc']

