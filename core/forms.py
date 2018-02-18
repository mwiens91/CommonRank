from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from timezone_field import TimeZoneFormField
from .models import User, Profile, Leaderboard, Match, Member

class ProfileSignUpForm(UserCreationForm):

    location = forms.CharField(max_length=30)
    timezone = TimeZoneFormField(initial='Canada/Pacific')
    bio = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                    'bio', 'location', 'timezone')

class LeaderboardSignUpForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        self.user=request.user
        member_queryset = Profile.objects.exclude(id=self.user.profile.id)
        super(LeaderboardSignUpForm, self).__init__(*args, **kwargs)
        self.fields['members'].queryset = member_queryset

    members = forms.ModelMultipleChoiceField(queryset=Profile.objects.none())

    class Meta:
        model = Leaderboard
        fields = ('name', 'info', 'members')

class CreateMatchSignUpForm(forms.ModelForm):

    OUTCOME_CHOICES = [['postpone', 'Schedule match for later'],
                       ['win', 'I won'],
                       ['loss', 'I lost']]

    def __init__(self, *args, **kwargs):
        leaderboard_id = kwargs.pop('leaderboard_id')
        my_id = kwargs.pop('my_id')
        member_queryset = Leaderboard.objects.get(id=leaderboard_id).member_set.exclude(id=my_id)
        super(CreateMatchSignUpForm, self).__init__(*args, **kwargs)
        self.fields['player2'].queryset = member_queryset

    player2 = forms.ModelChoiceField(queryset=Member.objects.none(),
                                     label="Opponent")
    outcome = forms.ChoiceField(choices=OUTCOME_CHOICES)

    class Meta:
        model = Match
        fields = ('player2', 'outcome')

class VerifyMatchSignUpForm(forms.ModelForm):

    class Meta:
        model = Match
        fields = ('winner', 'loser',)
