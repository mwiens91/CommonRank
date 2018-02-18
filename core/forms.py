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
    leaderboard_id = 1

    def __init__(self, *args, leaderboard_id,  **kwargs):
        self.leaderboard_id = leaderboard_id
        super(CreateMatchSignUpForm, self).__init__(*args, **kwargs)

    player2 = forms.ModelChoiceField(queryset=Leaderboard.objects.get(id=6).member_set)
    already_played = forms.BooleanField()
    did_win = forms.BooleanField()
    #player2 = forms.IntegerField()

    class Meta:
        model = Match
        fields = ('player2', 'already_played', 'did_win')
