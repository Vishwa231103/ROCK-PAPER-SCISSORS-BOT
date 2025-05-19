from RPS import player
import random

# Define opponent bots
def random_bot(prev):
    return random.choice(['R', 'P', 'S'])

def repeat_rock_bot(prev):
    return 'R'

def cycle_bot(prev):
    cycle = ['R', 'P', 'S']
    if not hasattr(cycle_bot, "index"):
        cycle_bot.index = 0
    move = cycle[cycle_bot.index]
    cycle_bot.index = (cycle_bot.index + 1) % 3
    return move

def copy_last_move_bot(prev):
    return prev if prev else random.choice(['R', 'P', 'S'])

# Determine winner: returns 1 if p1 wins, -1 if p2 wins, 0 if tie
def winner(p1, p2):
    if p1 == p2:
        return 0
    if (p1 == 'R' and p2 == 'S') or (p1 == 'P' and p2 == 'R') or (p1 == 'S' and p2 == 'P'):
        return 1
    return -1

# Run match
def run_match(opponent_func, rounds=1000):
    p1_prev = ''
    p2_prev = ''
    p1_score = 0
    p2_score = 0

    for _ in range(rounds):
        move2 = opponent_func(p1_prev)
        move1 = player(p2_prev)  # your player sees opponent's last move
        result = winner(move1, move2)
        if result == 1:
            p1_score += 1
        elif result == -1:
            p2_score += 1
        p1_prev = move1
        p2_prev = move2

    print(f"Against {opponent_func.__name__}: Your wins = {p1_score}, Opponent wins = {p2_score}, Win rate = {p1_score/rounds:.2%}")

if __name__ == "__main__":
    run_match(random_bot)
    run_match(repeat_rock_bot)
    run_match(cycle_bot)
    run_match(copy_last_move_bot)
