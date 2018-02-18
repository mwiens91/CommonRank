from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from core.models import Leaderboard, Member, Profile, User, Match
from core.forms import LeaderboardSignUpForm, ProfileSignUpForm, CreateMatchSignUpForm

@login_required
def leaderboard_create(request):
    """Leaderboard creation page."""
    if request.method == 'POST':
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

    # Get the member
    this_member = Member.objects.filter(profileuser__user_id=request.user.id)[0]

    # Get the top-N for the leaderboard
    toplist = thisleaderboard.member_set.order_by('-elo')
    N = 10 if len(toplist) > 10 else len(toplist)

    toplist = toplist[:N]

    return render(request,
                  'leaderboard_home.html',
                  {'leaderboard': thisleaderboard,
                   'member': this_member,
                   'topmembers': toplist,
                   'N': N})

@login_required
def leaderboard_rankings(request, leaderboard_id):
    """Leaderboard ranking page."""
    # Get the instance of this leaderboard
    thisleaderboard = Leaderboard.objects.get(id=leaderboard_id)

    # Get the members for the leaderboard, sorted by elo
    rankings = thisleaderboard.member_set.order_by('-elo')

    return render(request,
                  'leaderboard_rankings.html',
                  {'leaderboard': thisleaderboard,
                   'rankings': rankings})

@login_required
def leaderboard_admin(request, leaderboard_id):
    """Leaderboard Admin Page."""
    this_leaderboard = Leaderboard.objects.get(id=leaderboard_id)

    #Get all Members of leaderboard
    member_list = this_leaderboard.member_set

    return render(request,
                  'leaderboard_admin.html',
                  {'leaderboard': this_leaderboard,
                   'member_list': member_list})

def match_history(request, leaderboard_id):
    """Shows the match history of a leaderboard."""
    # Get the instance of this leaderboard
    thisleaderboard = Leaderboard.objects.get(id=leaderboard_id)

    # Get all of the matches of the leaderboard
    matches = thisleaderboard.match_set.all()

    return render(request,
                  'match_history.html',
                  {'leaderboard': thisleaderboard,
                   'matches': matches})

def match_verify_list(request, leaderboard_id, member_id):
    """Shows a list of matches a member needs to verify."""
    # Get the instance of this leaderboard
    thisleaderboard = Leaderboard.objects.get(id=leaderboard_id)

    # Get all of the matches of the leaderboard that the member needs to
    # verify
    matches = thisleaderboard.match_set.filter(loser_id=member_id).filter(state=1)

    return render(request,
                  'match_verify.html',
                  {'leaderboard': thisleaderboard,
                   'matches': matches})

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
            user.profile.location = form.cleaned_data.get('location')
            user.profile.timezone = form.cleaned_data.get('timezone')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = ProfileSignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def create_match(request, leaderboard_id):
    member_id = Member.objects.filter(profileuser__user_id=request.user.id)[0].id
    if request.method == 'POST':
        leaderboard = Leaderboard.objects.get(id=leaderboard_id)
        form = CreateMatchSignUpForm(request.POST, leaderboard_id=leaderboard_id, my_id=member_id)
        if form.is_valid():
            player1 = Member.objects.filter(profileuser__user_id=request.user.id)[0]
            player2 = form.cleaned_data['player2']
            if form.cleaned_data['already_played'] == True:
                if form.cleaned_data.get('winner') == True:
                    Match.objects.create(player1=player1, player2=player2, leaderboard=leaderboard, winner=player1, loser=player2, state=1)
                    return redirect(leaderboard_home, leaderboard_id=leaderboard_id)
                Match.objects.create(player1=player1, player2=player2, leaderboard=leaderboard,
                                     loser=player1, winner=player2, state=1)
                return redirect(leaderboard_home, leaderboard_id=leaderboard_id)
            Match.objects.create(player1=player1, player2=player2, leaderboard=leaderboard, state=0)
            return redirect(leaderboard_home, leaderboard_id=leaderboard_id)
    else:
        form = CreateMatchSignUpForm(leaderboard_id=leaderboard_id, my_id=member_id)
    return render(request, 'match_create.html', {'form': form})

@login_required
@require_POST
def verify_match(request, leaderboard_id, match_id):
    """Verify match results."""
    match = Match.objects.get(id=match_id)
    match.state = 2
    match.save()

    # Update ELO

    #if request.META['HTTP_ACCEPT'] == 'application/json':
    return JsonResponse({'match_id': match_id}, status=200)

@login_required
@require_POST
def delete_match(request, leaderboard_id, match_id):
    """Delete a match."""
    Match.objects.get(id=match_id).delete()

    return JsonResponse({'match_id': match_id}, status=200)
