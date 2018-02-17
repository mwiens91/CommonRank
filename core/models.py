from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True)
    bio = models.TextField(max_length=200,
                            null=True,
                            blank=False,)

    def __str__(self):
        return '%s' % self.user.username

class Leaderboard(models.Model):

    info = models.TextField(max_length=200,
                            null=True,
                            blank=False,)
    name = models.CharField(max_length=200,
                            null=True,
                            blank=False,)
    challenge_enabled = models.BooleanField(null=True, blank=True)

    deadline_time = models.IntegerField(blank=2100, null=True)
    deadline_length = models.IntegerField(blank=14, null=True)
    elo_sensitivity = models.FloatField(blank=0.5, null=False)


    def __str__(self):
        return '%s' % self.name

    def invite_member(self, profile):
        Member.objects.create(leaderboard=self, profileuser=profile)

    def delete_member(self, profile):
        Member.objects.get(profileuser=profile).delete()

    def enable_challenge(self):
        self.challenge_enabled = True

    def disable_challenge(self):
        self.challenge_enabled = False

    def toggle_challenge(self):
        if self.challenge_enabled == True:
            self.disable_challenge()
        else:
            self.enable_challenge()

    def set_challenge_deadline(self, hour, minute):
        self.deadline_time = (hour * 100) + minute

    def set_challenge_duration(self, days):
        self.deadline_length = days

    def set_sensitivity(self, sensitivity):
        self.elo_sensitivity = sensitivity

    def add_privilege(self, user):
        subject = Member.objects.get(profileuser=user)
        subject.increase_privilege()

    def remove_privilege(self, user):
        subject = Member.objects.get(profileuser=user)
        subject.decrese_privilege()

class Member(models.Model):

    leaderboard = models.ForeignKey(Leaderboard,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,)
    profileuser = models.ForeignKey(Profile,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,)
    elo = models.FloatField()
    privilege = models.IntegerField(default=1, null=False)

class Challenge(models.Model):

    challenger = models.ManyToManyField(Member,
                                        related_name='challenger',)
    challengee = models.ManyToManyField(Member,
                                        related_name='challengee',)
    leaderboard = models.ForeignKey(Leaderboard,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,)
    punishment = models.BooleanField()
    expiry = models.TimeField()

class Notification(models.Model):

    profileuser = models.ForeignKey(Profile,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,)

class Match(models.Model):

    player1 = models.ManyToManyField(Member,
                                        related_name='player1',)
    player2 = models.ManyToManyField(Member,
                                        related_name='player2',)
    leaderboard = models.ForeignKey(Leaderboard,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,)
    winner = models.ManyToManyField(Member,
                                        related_name='winner',)
    loser = models.ManyToManyField(Member,
                                        related_name='loser',)

class Report(models.Model):

    match = models.ForeignKey(Match,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,)
    details = models.TextField(max_length=200,
                                null=True,
                                blank=False,)
