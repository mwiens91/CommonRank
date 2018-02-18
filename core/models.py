from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from core.update_elo import update_elo

class Profile(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True)
    bio = models.TextField(max_length=200,
                            null=True,
                            blank=False)

    def __str__(self):
        return '%s' % self.user.username

class Leaderboard(models.Model):

    info = models.TextField(max_length=200,
                            null=True,
                            blank=False)
    name = models.CharField(max_length=200,
                            null=True,
                            blank=False)
    challenge_enabled = models.BooleanField(default=True)

    deadline_time = models.IntegerField(blank=2100, null=True)
    deadline_length = models.IntegerField(blank=14, null=True)
    elo_sensitivity = models.FloatField(default=0.5, null=False)


    def __str__(self):
        return '%s' % self.name

    def invite_member(self, profile):
        Member.objects.create(leaderboard=self, profileuser=profile, privilege=1)

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
        subject.remove_privilege()

    def approve_member(self, user):
        subject = Member.objects.get(profileuser=user)
        if subject.privilege == -1:
            subject.increase_privilege()

    def set_bio(self, message):
        if len(message > 200):
            return False
        else:
            self.info = message
            return True

    def delete_match(self, match):
        Match.objects.get(id=match.id).delete()

    def report_match(self, match, reason):
        Match.objects.get(id=match.id).report(reason)

class Member(models.Model):

    leaderboard = models.ForeignKey(Leaderboard,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)
    profileuser = models.ForeignKey(Profile,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)
    elo = models.FloatField()

    privilege = models.IntegerField(default=1, null=False)

    wins = models.PositiveIntegerField(default=0, null=False)
    losses = models.PositiveIntegerField(default=0, null=False)

    def __str__(self):
        return '%s' % self.profileuser.user.username

    def increase_privilege(self):
        if self.privilege <= 4:
            self.privilege += 1

    def remove_privilege(self):
        if self.privilege >= 0:
            self.privilege -= 1

    #only losers can verify matches
    def verify_match(self,match_id):
        match = Match.objects.get(pk=match_id)
        match.state = 2 #verified
        match.winner, match.loser = update_elo(match.winner,match.loser,1)

class Challenge(models.Model):

    challenger = models.ManyToManyField(Member,
                                        related_name='challenger')
    challengee = models.ManyToManyField(Member,
                                        related_name='challengee')
    leaderboard = models.ForeignKey(Leaderboard,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)
    punishment = models.BooleanField()
    expiry = models.TimeField()


class Notification(models.Model):

    profileuser = models.ForeignKey(Profile,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)


class Match(models.Model):

    player1 = models.ForeignKey(Member,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name='player1')
    player2 = models.ForeignKey(Member,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name='player2')
    leaderboard = models.ForeignKey(Leaderboard,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,)
    winner = models.ForeignKey(Member,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name='winner')
    loser = models.ForeignKey(Member,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True,
                                related_name='loser')
    state = models.IntegerField(default=0)
    #deadline = models.DateTimeField(blank=datetime.date.today() + datetime.timedelta(days=leaderboard.deadline_length), null=False)

    def __str__(self):
        return '%s || Match %s ' % (self.leaderboard.name, self.id)

    #create_match is called when a challenge is created or when a regular match is submitted. Creates match object and fills in necessary information, then calls add_match to add the match to the leaderboard
    def create_match(player1,player2,leaderboard_id):
       match = self.create(player1=player1,
               player2=player2,
               leaderboard=Leaderboard.objects.get(pk=leaderboard_id),
               state=0) #state 0 means challenged but not accepted yet)

class Report(models.Model):

    match = models.ForeignKey(Match,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    details = models.TextField(max_length=200,
                                null=True,
                                blank=False)

    def __str__(self):
        return '%s || Match %s || Report %s ' % (self.leaderboard.name,
                                             self.match.id,
                                             self.id)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
