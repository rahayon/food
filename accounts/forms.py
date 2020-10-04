from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, UserProfile



class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'class':'form-control'}))
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class ProfileForm(forms.ModelForm):

    class Meta:
        """Meta definition for Profileform."""

        model = UserProfile
        exclude = ('user',)
