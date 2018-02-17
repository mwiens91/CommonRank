from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Leaderboard
from .forms import LeaderboardForm

@login_required
def createleaderboard(request):

    if request.method == 'POST':
        newleaderboard = Leaderboard()
        newtourney.host = request.user.profile
        form = LeaderboardForm(request.POST, request.FILES, instance=newleaderboard)
        if form.is_valid():
            thisleaderboard = form.save()
            Member.objects.create(leaderboard=thisleaderboard,
                                profileuser=request.user.profile,
                                admin=True,)
            thisleaderboard.save()
            return redirect(home)
    else:
        form = LeaderboardForm(instance=Leaderboard())
    return render(request, 'createleadboard.html', {'form': form})

