from RPS import player
import random

def play_match(bot, player, num_games=1000):
    player_score = 0
    opponent_score = 0
    prev_play = ""
    for _ in range(num_games):
        opponent_move = bot(prev_play)
        player_move = player(prev_play)
        if beats(player_move, opponent_move):
            player_score += 1
        elif beats(opponent_move, player_move):
            opponent_score += 1
        prev_play = opponent_move
    return player_score / num_games * 100

def beats(one, two):
    return (one == "R" and two == "S") or (one == "S" and two == "P") or (one == "P" and two == "R")

def random_bot(_):
    return random.choice(["R", "P", "S"])

def quincy_bot(_):
    return "P"

def abbey_bot(prev_play, counter=[0]):
    counter[0] += 1
    return ["R", "P", "S"][counter[0] % 3]

def kris_bot(prev_play):
    if prev_play == "":
        return "R"
    return prev_play

if __name__ == "__main__":
    print("Testing opponent: random")
    print("Win rate:", play_match(random_bot, player))

    print("Testing opponent: quincy")
    print("Win rate:", play_match(quincy_bot, player))

    print("Testing opponent: abbey")
    print("Win rate:", play_match(abbey_bot, player))

    print("Testing opponent: kris")
    print("Win rate:", play_match(kris_bot, player))
