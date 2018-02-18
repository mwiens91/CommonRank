import math
#from core.models import Leaderboard, Member, Profile, User, Match

def update_elo(winner, loser):
    expected_winner = 1/(1+math.pow(10,((loser.elo-winner.elo)/400)))
    expected_loser = 1 - expected_winner
    winner.elo = winner.elo + 32*(1-expected_winner)
    loser.elo = loser.elo + 32*(0-expected_loser)

