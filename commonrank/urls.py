"""commonrank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from core import views as core_views

urlpatterns = [
    path(r'', core_views.profile_home, name='home'),
    path(r'admin/', admin.site.urls),
    path(r'leaderboard/<int:leaderboard_id>/', core_views.leaderboard_home, name='leaderboard_home'),
    path(r'leaderboard/create/', core_views.leaderboard_create, name='leaderboard_signup'),
    path(r'leaderboard/<int:leaderboard_id>/match/create', core_views.create_match, name='match_create'),
    path(r'leaderboard/<int:leaderboard_id>/match/<int:match_id>/remove', core_views.delete_match, name='match_remove'),
    path(r'leaderboard/<int:leaderboard_id>/match/<int:match_id>/verify', core_views.verify_match, name='match_verify'),
    path(r'leaderboard/<int:leaderboard_id>/member/<int:member_id>/verify_matches', core_views.match_verify_list, name='match_verify_list'),
    path(r'leaderboard/<int:leaderboard_id>/match_history', core_views.match_history, name='match_history'),
    path(r'leaderboard/<int:leaderboard_id>/rankings', core_views.leaderboard_rankings, name='leaderboard_rankings'),
    path(r'login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path(r'logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path(r'signup/', core_views.profile_signup, name='signup'),
    path(r'invitations/', include('invitations.urls', namespace='invitations')),
]
