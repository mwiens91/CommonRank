import math
#from core.models import Leaderboard, Member, Profile, User, Match

#winner and loser are members, elo_sensitivity is a float from 0 to 1 inclusive
def update_elo(winner, loser, elo_sensitivity):
    winner_games = winner.wins + winner.losses
    loser_games = loser.wins + loser.losses
    if elo_sensitivity < 0.167:
        k_factor = 8
    elif elo_sensitivity < 0.334:
        k_factor = 16
    elif elo_sensitivity <= 0.5:
        k_factor = 24
    elif elo_sensitivity <= 0.667:
        k_factor = 32
    elif elo_sensitivity <= 0.834:
        k_factor = 40
    else:
        k_factor = 48
    winner_k_factor = k_factor
    loser_k_factor = k_factor
    expected_winner = 1/(1+math.pow(10,((loser.elo-winner.elo)/400)))
    expected_loser = 1 - expected_winner
    if(winner_games<20 and winner_games>=10):
        winner_k_factor = winner_k_factor*2
    elif(winner_games<10 and winner_games>=0):
        winner_k_factor = winner_k_factor*4
    if(loser_games<20 and loser_games>=10):
        loser_k_factor = loser_k_factor*2
    elif(loser_games<10 and loser_games>=0):
        loser_k_factor = loser_k_factor*4

    loser.elo = loser.elo + loser_k_factor*(0-expected_loser)
    winner.elo = winner.elo + winner_k_factor*(1-expected_winner)

    # Increment wins and losses
    loser.losses += 1
    winner.wins += 1

    # Update the loser and winner instances
    loser.save()
    winner.save()
