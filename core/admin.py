from django.contrib import admin
from core.models import Leaderboard, Member, Profile, Challenge, Notification, Match, Report

class MemberInline(admin.TabularInline):
    """Show the members of a leaderboard."""
    model = Member

class NotificationInline(admin.TabularInline):
    """ Show the notfications of a profile """
    model = Notification


class ReportInline(admin.TabularInline):
    """ Show the reports of a match """
    model = Report

class LeaderboardAdmin(admin.ModelAdmin):
     class MatchInline(admin.TabularInline):
         """Show the matches of a member """
         model = Match
     inlines = (MemberInline, MatchInline,)

class ProfileAdmin(admin.ModelAdmin):
    inlines = (MemberInline, NotificationInline)

class MemberAdmin(admin.ModelAdmin):
    class MatchInline(admin.TabularInline):
        """Show the matches of a member """
        model = Match
        fk_name = 'player1'

    inlines = (MatchInline,)

class MatchAdmin(admin.ModelAdmin):
    inlines = (ReportInline,)

admin.site.register(Leaderboard, LeaderboardAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Challenge)
admin.site.register(Notification)
admin.site.register(Match, MatchAdmin)
admin.site.register(Report)
