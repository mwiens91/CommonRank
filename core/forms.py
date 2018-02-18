from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User, Profile, Leaderboard, Match, Member

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
        fields = ('name', 'info', 'members','deadline_time','deadline_length')

class CreateMatchSignUpForm(forms.ModelForm):
    leaderboard_id = 0

    def __init__(self, leaderboard_id):
        self.leaderboard_id = leaderboard_id

    #members = forms.ModelChoiceField(queryset=Leaderboard.objects.get(id=leaderboard_id).member_set)
    already_played = forms.BooleanField()
    winner = forms.BooleanField()

    class Meta:
        model = Match
        fields = ('player2', 'already_played', 'winner')
