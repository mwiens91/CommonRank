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

class Leaderboard(models.Model)

    info = models.TextField(max_length=200,
                            null=True,
                            blank=False,)
    name = models.CharField(max_length=200,
                            null=True,
                            blank=False,)
    def __str__(self):
        return '%s' % self.name

class Member(models.Model)

    leaderboard = models.ForeignKey(Leaderboard,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,)
    profileuser = models.ForeignKey(Profile,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,)
    elo = models.FloatField(default='1500')
    admin = models.BooleanField()

class Challenge(models.Model)

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

class Notification(models.Model)

    profileuser = models.ForeignKey(Profile,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,)

class Match(models.Model)

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

class Report(models.Model)

    match = models.ForeignKey(Match,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,)
    details = models.TextField(max_length=200,
                                null=True,
                                blank=False,)
