from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User, Profile

class ProfileSignUpForm(UserCreationForm):

    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email'
                    'bio')

