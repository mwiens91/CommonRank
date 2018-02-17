from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User, Profile, Leaderboard

class ProfileSignUpForm(UserCreationForm):

    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                    'bio')

class LeaderboardSignUpForm(forms.ModelForm):

    members = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    class Meta:
        model = Leaderboard
        fields = ('name', 'info', 'members','deadline_time','deadline_length',)
