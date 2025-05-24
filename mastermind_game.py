"""
Run this file to see the three bots attempt to play mastermind.

Their settings are as follows:
- BI 0: randomly guesses each turn
- BI 1: randomly selects from allowed moves following previous turn
- BI 2: randomly selects from allowed moves following best previous turn

Please adjust the parameters in the 'CHOOSE PARAMTERS' section below.
"""

# import required modules
import numpy as np
import pandas as pd
from random import randint as rand
from matplotlib import pyplot as plt

######### CHOOSE PARAMETERS #########
max_turns = 100
total_game_count = 100
show_games = "y"
#####################################

# create colours
colours = ["y","g","b","p","v","o"]

# helper function that initiates parameters at the start of each game
def initialise_game_state():
    return {
        "row_vector": [],
        "evaluation_vector": [],
        "guess_list": [],
        "evaluation_list": [],
        "score_list": [],
        "current_guess": ["*", "*", "*", "*"],
        "turn_number": 0,
        "solution": [],
        "bot_intelligence": 0,
        "game_end": False
    }

# helper function that prints game board
def print_board(game_state):
    print('\n'.join([m+n for m,n in zip(game_state["row_vector"],game_state["evaluation_vector"])]))

# helper function that returns an evaluation for a given guess
def checker(game_state):
    evaluation = []
    solution = game_state["solution"]
    current_guess = game_state["current_guess"]
    solution_reduced = solution.copy()
    current_guess_reduced = current_guess.copy()
    for i in range(4):
        if current_guess[i] == solution[i]:
            evaluation.append("r")
            solution_reduced[i] = "x"
            current_guess_reduced[i] = "z"
    for i in range(4):
        if current_guess_reduced[i] in solution_reduced:
            evaluation.append("w")
            solution_reduced[solution_reduced.index(current_guess_reduced[i])] = "x"
            current_guess_reduced[i] = "z"
    evaluation = sorted(evaluation)
    game_state["evaluation_list"].append(evaluation)
    return evaluation
    #print(f"Your score is {evaluation}.")

# helper function that scores guesses based on evaluation, allowing evaluations to be ranked
def guess_score(game_state, evaluation):
    if evaluation == []:
        score = 0
    elif evaluation == ["w"]:
        score = 1
    elif evaluation == ["w","w"]:
        score = 2
    elif evaluation == ["r"] or evaluation == ["r","w"]:
        score = 3
    elif evaluation == ["w","w","w"]:
        score = 4
    elif evaluation == ["r","r"] or evaluation == ["r","w","w"]:
        score = 5
    elif evaluation == ["r","r","w"]:
        score = 6
    elif evaluation == ["r","r","r"]:
        score = 7
    elif evaluation == ["w","w","w","w"]:
        score = 8
    elif evaluation == ["r","w","w","w"]:
        score = 9
    elif evaluation == ["r","r","w","w"]:
        score = 10
    elif evaluation == ["r","r","r","r"]:
        score = 11
    game_state["score_list"].append(score)
    return score

# helper function that decides the next move based on the previous evaluation
def next_move_decider(game_state, evaluation):
    #print(f"MY CURRENT MOVE IS {game_state["current_guess"]}")
    #print(f"turn number: {game_state["turn_number"]}")
    if game_state["bot_intelligence"] == 0 or evaluation == []:
        guess_try = [colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)]]
    elif evaluation == ["r","r","r"]:
        guess_try = rrr_function(game_state["current_guess"])[rand(0,3)]
    elif evaluation == ["r"]:
        guess_try = r_function(game_state["current_guess"])[rand(0,3)]
    elif evaluation == ["r","r","w","w"]:
        guess_try = rrww_function(game_state["current_guess"])[rand(0,5)]
    elif evaluation == ["r","r"]:
        guess_try = rr_function(game_state["current_guess"])[rand(0,5)]
    elif evaluation == ["r","w","w","w"]:
        guess_try = rwww_function(game_state["current_guess"])[rand(0,7)]
    elif evaluation == ["w","w","w","w"]:
        guess_try = wwww_function(game_state["current_guess"])[rand(0,8)]
    elif evaluation == ["r","r","w"]:
        guess_try = rrw_function(game_state["current_guess"])[rand(0,11)]
    elif evaluation == ["w"]:
        guess_try = w_function(game_state["current_guess"])[rand(0,11)]
    elif evaluation == ["r","w"]:
        guess_try = rw_function(game_state["current_guess"])[rand(0,23)]
    elif evaluation == ["r","w","w"]:
        guess_try = rww_function(game_state["current_guess"])[rand(0,35)]
    elif evaluation == ["w","w"]:
        guess_try = ww_function(game_state["current_guess"])[rand(0,41)]
    elif evaluation == ["w","w","w"]:
        guess_try = www_function(game_state["current_guess"])[rand(0,46)]
    if guess_try in game_state["guess_list"]:
        next_move_decider(game_state, evaluation)
    return guess_try

### compendium of possible permutations for each evaluation
# rrww --> 6 combinations
def rrww_function(guess):
    moves_rrww = [
        [guess[0],guess[1],guess[3],guess[2]],
        [guess[0],guess[3],guess[2],guess[1]],
        [guess[0],guess[2],guess[1],guess[3]],
        [guess[3],guess[1],guess[2],guess[0]],
        [guess[2],guess[1],guess[0],guess[3]],
        [guess[1],guess[0],guess[2],guess[3]]
        ]
    return moves_rrww

# rwww --> 8 combinations
def rwww_function(guess):
    moves_rwww = [
        [guess[0],guess[3],guess[1],guess[2]],
        [guess[0],guess[2],guess[3],guess[1]],
        [guess[3],guess[1],guess[0],guess[2]],
        [guess[2],guess[1],guess[3],guess[0]],
        [guess[3],guess[0],guess[2],guess[1]],
        [guess[1],guess[3],guess[2],guess[0]],
        [guess[2],guess[0],guess[1],guess[3]],
        [guess[1],guess[2],guess[0],guess[3]]
        ]
    return moves_rwww

# wwww --> 9 combinations
def wwww_function(guess):
    moves_wwww = [
        [guess[3],guess[0],guess[1],guess[2]],
        [guess[3],guess[2],guess[0],guess[1]],
        [guess[3],guess[2],guess[1],guess[0]],
        [guess[2],guess[3],guess[0],guess[1]],
        [guess[2],guess[3],guess[1],guess[0]],
        [guess[2],guess[0],guess[3],guess[1]],
        [guess[1],guess[2],guess[3],guess[0]],
        [guess[1],guess[0],guess[3],guess[2]],
        [guess[1],guess[3],guess[0],guess[2]]
        ]
    return moves_wwww

# rrr --> 4 combinations
def rrr_function(guess):
    moves_rrr = [
        [guess[0],guess[1],guess[2],colours[rand(0,5)]],
        [guess[0],guess[1],colours[rand(0,5)],guess[3]],
        [guess[0],colours[rand(0,5)],guess[2],guess[3]],
        [colours[rand(0,5)],guess[1],guess[2],guess[3]]
        ]
    return moves_rrr

# rrw --> 12 combinations
def rrw_function(guess):
    moves_rrw = [
        [guess[0],guess[1],guess[3],colours[rand(0,5)]],
        [guess[0],guess[1],colours[rand(0,5)],guess[2]],
        [guess[0],guess[3],guess[2],colours[rand(0,5)]],
        [guess[0],colours[rand(0,5)],guess[2],guess[1]],
        [guess[0],guess[2],colours[rand(0,5)],guess[3]],
        [guess[0],colours[rand(0,5)],guess[1],guess[3]],
        [guess[3],guess[1],guess[2],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[1],guess[2],guess[0]],
        [guess[2],guess[1],colours[rand(0,5)],guess[3]],
        [colours[rand(0,5)],guess[1],guess[0],guess[3]],
        [guess[1],colours[rand(0,5)],guess[2],guess[3]],
        [colours[rand(0,5)],guess[0],guess[2],guess[3]],
        ]
    return moves_rrw

# rww --> 36 combinations
def rww_function(guess):
    moves_rww = [
        [guess[0],guess[2],guess[1],colours[rand(0,5)]],
        [guess[0],guess[3],guess[1],colours[rand(0,5)]],
        [guess[0],guess[2],guess[3],colours[rand(0,5)]],
        [guess[2],guess[1],guess[0],colours[rand(0,5)]],
        [guess[3],guess[1],guess[0],colours[rand(0,5)]],
        [guess[2],guess[1],guess[3],colours[rand(0,5)]],
        [guess[1],guess[0],guess[2],colours[rand(0,5)]],
        [guess[3],guess[0],guess[2],colours[rand(0,5)]],
        [guess[1],guess[3],guess[2],colours[rand(0,5)]],
        [guess[0],guess[2],colours[rand(0,5)],guess[1]],
        [guess[0],guess[3],colours[rand(0,5)],guess[1]],
        [guess[0],guess[3],colours[rand(0,5)],guess[2]],
        [guess[2],guess[1],colours[rand(0,5)],guess[0]],
        [guess[3],guess[1],colours[rand(0,5)],guess[0]],
        [guess[3],guess[1],colours[rand(0,5)],guess[2]],
        [guess[1],guess[0],colours[rand(0,5)],guess[3]],
        [guess[2],guess[0],colours[rand(0,5)],guess[3]],
        [guess[1],guess[2],colours[rand(0,5)],guess[3]],
        [guess[0],colours[rand(0,5)],guess[1],guess[2]],
        [guess[0],colours[rand(0,5)],guess[3],guess[1]],
        [guess[0],colours[rand(0,5)],guess[3],guess[2]],
        [guess[1],colours[rand(0,5)],guess[2],guess[0]],
        [guess[3],colours[rand(0,5)],guess[2],guess[0]],
        [guess[3],colours[rand(0,5)],guess[2],guess[1]],
        [guess[1],colours[rand(0,5)],guess[0],guess[3]],
        [guess[2],colours[rand(0,5)],guess[0],guess[3]],
        [guess[2],colours[rand(0,5)],guess[1],guess[3]],
        [colours[rand(0,5)],guess[1],guess[0],guess[2]],
        [colours[rand(0,5)],guess[1],guess[3],guess[0]],
        [colours[rand(0,5)],guess[1],guess[3],guess[2]],
        [colours[rand(0,5)],guess[0],guess[2],guess[1]],
        [colours[rand(0,5)],guess[3],guess[2],guess[0]],
        [colours[rand(0,5)],guess[3],guess[2],guess[1]],
        [colours[rand(0,5)],guess[0],guess[1],guess[3]],
        [colours[rand(0,5)],guess[2],guess[0],guess[3]],
        [colours[rand(0,5)],guess[2],guess[1],guess[3]],
        ]
    return moves_rww

# www --> 47 combinations
def www_function(guess):
    moves_www = [
        [guess[2],guess[0],guess[1],colours[rand(0,5)]],
        [guess[1],guess[2],guess[0],colours[rand(0,5)]],
        [guess[2],guess[0],colours[rand(0,5)],guess[1]],
        [guess[1],guess[2],colours[rand(0,5)],guess[0]],
        [guess[1],guess[0],colours[rand(0,5)],guess[2]],
        [guess[1],colours[rand(0,5)],guess[0],guess[2]],
        [guess[2],colours[rand(0,5)],guess[0],guess[1]],
        [guess[2],colours[rand(0,5)],guess[1],guess[0]],
        [colours[rand(0,5)],guess[0],guess[1],guess[2]],
        [colours[rand(0,5)],guess[0],guess[2],guess[1]],
        [colours[rand(0,5)],guess[2],guess[0],guess[1]],
        [colours[rand(0,5)],guess[2],guess[1],guess[0]],
        [guess[1],guess[0],guess[3],colours[rand(0,5)]],
        [guess[1],guess[3],guess[0],colours[rand(0,5)]],
        [guess[3],guess[0],guess[1],colours[rand(0,5)]],
        [guess[1],guess[3],colours[rand(0,5)],guess[0]],
        [guess[3],guess[0],colours[rand(0,5)],guess[1]],
        [guess[1],colours[rand(0,5)],guess[3],guess[0]],
        [guess[3],colours[rand(0,5)],guess[0],guess[1]],
        [guess[3],colours[rand(0,5)],guess[1],guess[0]],
        [colours[rand(0,5)],guess[0],guess[3],guess[1]],
        [colours[rand(0,5)],guess[1],guess[3],guess[0]],
        [colours[rand(0,5)],guess[3],guess[0],guess[1]],
        [colours[rand(0,5)],guess[3],guess[1],guess[0]],
        [guess[2],guess[0],guess[3],colours[rand(0,5)]],
        [guess[2],guess[3],guess[0],colours[rand(0,5)]],
        [guess[3],guess[2],guess[0],colours[rand(0,5)]],
        [guess[2],guess[3],colours[rand(0,5)],guess[0]],
        [guess[3],guess[0],colours[rand(0,5)],guess[2]],
        [guess[3],guess[2],colours[rand(0,5)],guess[0]],
        [guess[2],colours[rand(0,5)],guess[3],guess[0]],
        [guess[3],colours[rand(0,5)],guess[0],guess[2]],
        [colours[rand(0,5)],guess[0],guess[3],guess[2]],
        [colours[rand(0,5)],guess[2],guess[3],guess[0]],
        [colours[rand(0,5)],guess[3],guess[0],guess[2]],
        [colours[rand(0,5)],guess[3],guess[2],guess[0]],
        [guess[1],guess[2],guess[3],colours[rand(0,5)]],
        [guess[2],guess[3],guess[1],colours[rand(0,5)]],
        [guess[3],guess[2],guess[1],colours[rand(0,5)]],
        [guess[1],guess[3],colours[rand(0,5)],guess[2]],
        [guess[2],guess[3],colours[rand(0,5)],guess[1]],
        [guess[3],guess[2],colours[rand(0,5)],guess[1]],
        [guess[1],colours[rand(0,5)],guess[3],guess[2]],
        [guess[2],colours[rand(0,5)],guess[3],guess[1]],
        [guess[3],colours[rand(0,5)],guess[1],guess[2]],
        [colours[rand(0,5)],guess[2],guess[3],guess[1]],
        [colours[rand(0,5)],guess[3],guess[1],guess[2]],
        ]
    return moves_www

# rr --> 6 combinations
def rr_function(guess):
    moves_rr = [
        [guess[0],guess[1],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[0],colours[rand(0,5)],guess[2],colours[rand(0,5)]],
        [guess[0],colours[rand(0,5)],colours[rand(0,5)],guess[3]],
        [colours[rand(0,5)],guess[1],guess[2],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[1],colours[rand(0,5)],guess[3]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[2],guess[3]]
        ]
    return moves_rr

# rw --> 24 combinations
def rw_function(guess):
    moves_rw = [
        [guess[0],guess[2],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[0],guess[3],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[2],guess[1],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[3],guess[1],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[0],colours[rand(0,5)],guess[1],colours[rand(0,5)]],
        [guess[0],colours[rand(0,5)],guess[3],colours[rand(0,5)]],
        [guess[1],colours[rand(0,5)],guess[2],colours[rand(0,5)]],
        [guess[3],colours[rand(0,5)],guess[2],colours[rand(0,5)]],
        [guess[0],colours[rand(0,5)],colours[rand(0,5)],guess[1]],
        [guess[0],colours[rand(0,5)],colours[rand(0,5)],guess[2]],
        [guess[1],colours[rand(0,5)],colours[rand(0,5)],guess[3]],
        [guess[2],colours[rand(0,5)],colours[rand(0,5)],guess[3]],
        [colours[rand(0,5)],guess[1],guess[0],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[1],guess[3],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[0],guess[2],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[3],guess[2],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[1],colours[rand(0,5)],guess[0]],
        [colours[rand(0,5)],guess[1],colours[rand(0,5)],guess[2]],
        [colours[rand(0,5)],guess[0],colours[rand(0,5)],guess[3]],
        [colours[rand(0,5)],guess[2],colours[rand(0,5)],guess[3]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[2],guess[0]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[2],guess[1]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[0],guess[3]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[1],guess[3]]
        ]
    return moves_rw

# ww --> 42 combinations
def ww_function(guess):
    moves_ww = [
        [guess[1],guess[0],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[1],guess[2],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[1],guess[3],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[2],guess[0],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[2],guess[3],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[3],guess[0],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[3],guess[2],colours[rand(0,5)],colours[rand(0,5)]],
        [guess[1],colours[rand(0,5)],guess[0],colours[rand(0,5)]],
        [guess[1],colours[rand(0,5)],guess[3],colours[rand(0,5)]],
        [guess[2],colours[rand(0,5)],guess[0],colours[rand(0,5)]],
        [guess[2],colours[rand(0,5)],guess[1],colours[rand(0,5)]],
        [guess[2],colours[rand(0,5)],guess[3],colours[rand(0,5)]],
        [guess[3],colours[rand(0,5)],guess[0],colours[rand(0,5)]],
        [guess[3],colours[rand(0,5)],guess[1],colours[rand(0,5)]],
        [guess[1],colours[rand(0,5)],colours[rand(0,5)],guess[0]],
        [guess[1],colours[rand(0,5)],colours[rand(0,5)],guess[2]],
        [guess[2],colours[rand(0,5)],colours[rand(0,5)],guess[0]],
        [guess[2],colours[rand(0,5)],colours[rand(0,5)],guess[1]],
        [guess[3],colours[rand(0,5)],colours[rand(0,5)],guess[0]],
        [guess[3],colours[rand(0,5)],colours[rand(0,5)],guess[1]],
        [guess[3],colours[rand(0,5)],colours[rand(0,5)],guess[2]],
        [colours[rand(0,5)],guess[0],guess[1],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[0],guess[3],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[2],guess[0],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[2],guess[1],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[2],guess[3],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[3],guess[0],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[3],guess[1],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[0],colours[rand(0,5)],guess[1]],
        [colours[rand(0,5)],guess[0],colours[rand(0,5)],guess[2]],
        [colours[rand(0,5)],guess[2],colours[rand(0,5)],guess[0]],
        [colours[rand(0,5)],guess[2],colours[rand(0,5)],guess[1]],
        [colours[rand(0,5)],guess[3],colours[rand(0,5)],guess[0]],
        [colours[rand(0,5)],guess[3],colours[rand(0,5)],guess[1]],
        [colours[rand(0,5)],guess[3],colours[rand(0,5)],guess[2]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[0],guess[1]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[0],guess[2]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[1],guess[0]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[1],guess[2]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[3],guess[0]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[3],guess[1]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[3],guess[2]]
        ]
    return moves_ww

# r --> 4 combinations
def r_function(guess):
    moves_r = [
        [guess[0],colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[1],colours[rand(0,5)],colours[rand(0,5)]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[2],colours[rand(0,5)]],
        [colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)],guess[3]]
        ]
    return moves_r

# w --> 12 combinations
def w_function(guess):
    moves_w = [
        [colours[rand(0,5)],guess[0],colours[rand(0,5)],colours[rand(0,5)]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[0],colours[rand(0,5)]],
        [colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)],guess[0]],
        [guess[1],colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[1],colours[rand(0,5)]],
        [colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)],guess[1]],
        [guess[2],colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[2],colours[rand(0,5)],colours[rand(0,5)]],
        [colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)],guess[2]],
        [guess[3],colours[rand(0,5)],colours[rand(0,5)],colours[rand(0,5)]],
        [colours[rand(0,5)],guess[3],colours[rand(0,5)],colours[rand(0,5)]],
        [colours[rand(0,5)],colours[rand(0,5)],guess[3],colours[rand(0,5)]]
        ]
    return moves_w

# main function
def play_mastermind(max_turns, total_game_count, show_games):
    game_state = initialise_game_state()
    game_number = 0
    session_summary_df = pd.DataFrame(columns=["Game","Attempts"])
    # prepare output_df for ML
    output_df = pd.DataFrame(columns=np.arange(1,max_turns+2).tolist())
    output_df.columns = [*output_df.columns[:-1],"bot_intelligence"]
    #loop through games
    while game_number < total_game_count:
        game_state = initialise_game_state()
        game_state["bot_intelligence"] = game_number % 3 #(every third game runs the same intelligence level)
        game_number += 1
        game_state["solution"] = [colours[rand(0,5)] for i in range(4)]
        if show_games == "y":
            print(f"Game: {game_number}\nBot Intelligence: {game_state["bot_intelligence"]}\nSolution: {game_state["solution"]}")
        #loop through turns
        while game_state["game_end"] == False:
            game_state["turn_number"] += 1
            if game_state["current_guess"] == ["*","*","*","*"]:
                random_vector = [rand(0,5) for i in range(4)]
                a_s = colours[random_vector[0]]
                b_s = colours[random_vector[1]]
                c_s = colours[random_vector[2]]
                d_s = colours[random_vector[3]]
                game_state["current_guess"] = [a_s,b_s,c_s,d_s]
                #print(f"Guess: {game_state["current_guess"]}")
            evaluation = checker(game_state)
            game_state["row_vector"].append(" ".join(game_state["current_guess"]))
            game_state["evaluation_vector"].append("--> "+"".join(str(i) for i in evaluation))
            score = guess_score(game_state, evaluation)
            if evaluation == ["r","r","r","r"]:
                if show_games == "y":
                    print_board(game_state)
                    print(f"Bot wins with {game_state["turn_number"]} turns!\n")
                session_summary_df.loc[len(session_summary_df)] = [game_number,game_state["turn_number"]]
                if len(game_state["score_list"]) < max_turns:
                    game_state["score_list"].extend([11 for i in range(max_turns-len(game_state["score_list"]))])
                else:
                    game_state["score_list"] = game_state["score_list"][:max_turns]
                game_state["score_list"].append(game_state["bot_intelligence"])
                output_df.loc[len(output_df)] = game_state["score_list"]
                game_state["game_end"] = True
            elif game_state["turn_number"] == max_turns:
                if show_games == "y":
                    print_board(game_state)
                    print("Bot lost.\n")
                session_summary_df.loc[len(session_summary_df)] = [game_number,"Failed"]
                if len(game_state["score_list"]) < max_turns:
                    game_state["score_list"].extend([11 for i in range(max_turns-len(game_state["score_list"]))])
                else:
                    game_state["score_list"] = game_state["score_list"][:max_turns]
                game_state["score_list"].append(game_state["bot_intelligence"])
                output_df.loc[len(output_df)] = game_state["score_list"]
                game_state["game_end"] = True
            else:
                game_state["guess_list"].append(game_state["current_guess"])
                #guess_score(game_state, evaluation)
                if game_state["bot_intelligence"] == 2 and score < max(game_state["score_list"]):
                    guess_try = game_state["guess_list"][game_state["score_list"].index(max(game_state["score_list"]))]
                    evaluation = game_state["evaluation_list"][game_state["score_list"].index(max(game_state["score_list"]))]
                    #print(f'Returning to turn {game_state["score_list"].index(max(game_state["score_list"]))} - having guess {game_state["guess_list"][game_state["score_list"].index(max(game_state["score_list"]))]} and evaluation {game_state["evaluation_list"][game_state["score_list"].index(max(game_state["score_list"]))]}')
                if game_state["turn_number"] > 1:
                    game_state["current_guess"] = guess_try
                guess_try = next_move_decider(game_state, evaluation)
                game_state["current_guess"] = guess_try
                #print(f"Guess: {game_state["current_guess"]}")
                # game_state["guess_list"].append(game_state["current_guess"])
        if game_number == total_game_count:
            if show_games == "y":
                print("-- END OF SESSION --")
            print(session_summary_df)
            #print(f"Mean: {round(session_summary_df.mean()[1],2)}\nStandard Deviation: {round(session_summary_df.std()[1],2)}")
            output_df = output_df.apply(pd.to_numeric)
            print(output_df)
            print(f"Means:\n{output_df.groupby('bot_intelligence',as_index=False)[[i for i in range(1,max_turns+1)]].mean()}")
            to_graph = output_df.groupby('bot_intelligence',as_index=False)[[i for i in range(1,max_turns+1)]].mean().transpose().rename(columns={0:"BI 0",1:"BI 1",2:"BI 2"})
            to_graph.drop(index=to_graph.index[0],axis=0,inplace=True)
            print(to_graph)
            plt.plot(to_graph["BI 2"],label="BI 2")
            plt.plot(to_graph["BI 1"],label="BI 1")
            plt.plot(to_graph["BI 0"],label="BI 0")
            plt.axhline(y=11, color='black', linestyle='--')
            plt.xlabel("Number of Turns")
            plt.ylabel("Mean Score")
            plt.yticks([i for i in range(12)])
            plt.legend(loc="lower right")
            plt.show()
            #print(f'BI 2 Success: {to_graph["BI 2"].tolist().index(11)}')
            #print(f'BI 1 Success: {to_graph["BI 1"].tolist().index(11)}')
            #print(f'BI 0 Success: {to_graph["BI 0"].tolist().index(11)}')

play_mastermind(max_turns, total_game_count, show_games)