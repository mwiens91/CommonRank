from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from core.models import Leaderboard, Member, Profile, User
from core.forms import LeaderboardSignUpForm, ProfileSignUpForm

@login_required
def leaderboard_create(request):
    """Leaderboard creation page."""
    if request.method == 'POST':
        newtourney.host = request.user.profile
        form = LeaderboardSignUpForm(request.POST)
        if form.is_valid():
            thisleaderboard = form.save()
            Member.objects.create(leaderboard=thisleaderboard,
                                profileuser=request.user.profile,
                                privilege=5, elo=69)
            thisleaderboard.save()
            return redirect(leaderboard_home,
                            leaderboard_id=thisleaderboard.id)
    else:
        form = LeaderboardSignUpForm(instance=Leaderboard())
    return render(request, 'leaderboard_signup.html', {'form': form})

@login_required
def leaderboard_home(request, leaderboard_id):
    """Leaderboard home page."""
    # Get the instance of this leaderboard
    thisleaderboard = Leaderboard.objects.get(id=leaderboard_id)

    # Get the top-N for the leaderboard
    N = 10
    toplist = thisleaderboard.member_set.order_by('-elo')

    if length(toplist) > 10:
        toplist = toplist[:10]

    return render(request,
                  'leaderboard_home.html',
                  {'leaderboard': thisleaderboard,
                   'topmemebers': toplist})

@login_required
def profile_home(request):
    """Profile home page."""
    # Get all of a profile's leaderboards
    members = request.user.profile.member_set.all()
    leaderboards = [member.leaderboard for member in members]

    # Get all of a profile's notifications
    notifications = request.user.profile.notification_set.all()

    return render(request, 'home.html', {'leaderboards': leaderboards,
                                         'notifications': notifications})

def profile_signup(request):
    """Profile sign up page."""
    if request.method == 'POST':
        form = ProfileSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.bio = form.cleaned_data.get('bio')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(home)
    else:
        form = ProfileSignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def create_match(request):
    """Create Match Page"""
    if request.method == 'POST':
        leaderboard = Leaderboard.objects.get(id=form.leaderboard.id)
        form = CreateMatchSignUpForm(request.POST, leaderboard_id=leaderboard.id)
        if form.is_valid():
            Match.objects.create(player1=request.user.profile, player2=form.player2, Leaderboard=leaderboard)
            form.save()
            return redirect(home)
    else:
        form = CreateMatchSignUpForm(instance=Match())
    return render(request, 'create-match.html', {'form': form})
