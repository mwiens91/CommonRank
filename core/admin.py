from django.contrib import admin
from core.models import Leaderboard, Member, Profile, Challenge, Notification, Match, Report

class MemberInline(admin.TabularInline):
    """Show the members of a leaderboard."""
    model = Member

class NotitficationInline(admin.TabularInline):
    """ Show the notfications of a profile """
    model = Notification

class MatchInline(admin.TabularInline):
    """ Show the matches of a member """
    model = Match

class ReportInline(admin.TabularInline):
    """ Show the reports of a match """
    model = Report

class LeaderboardAdmin(admin.ModelAdmin):
    inlines = (MemberInline, MatchInline,)

class ProfileAdmin(admin.ModelAdmin):
    inlines = (MemberInline, NotificationInline)

class MemberAdmin(admin.ModelAdmin):
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
