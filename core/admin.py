from django.contrib import admin
from core.models import Leaderboard, Member, Profile

class MemberInline(admin.TabularInline):
    """Show the members of a leaderboard."""
    model = Member

class LeaderboardAdmin(admin.ModelAdmin):
    inlines = (MemberInline,)

admin.site.register(Leaderboard, LeaderboardAdmin)
admin.site.register(Profile)
