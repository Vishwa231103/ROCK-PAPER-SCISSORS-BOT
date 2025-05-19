import tkinter as tk
from tkinter import ttk
import random
from collections import Counter

# --- Adaptive Bot (same as your player function) ---
def adaptive_player(prev_play, opponent_history=[], my_history=[], strategy_scores={'freq':0, 'pattern':0, 'cycle':0}, round_num=[0]):
    if prev_play:
        opponent_history.append(prev_play)

    round_num[0] += 1

    beats_map = {'R': 'P', 'P': 'S', 'S': 'R'}

    # Strategy 1: Frequency
    freq_move = 'R'
    if opponent_history:
        most_common = Counter(opponent_history).most_common(1)[0][0]
        freq_move = beats_map[most_common]

    # Strategy 2: Pattern
    pattern_move = 'R'
    pattern_length = 3
    guess_map = {}
    if len(opponent_history) >= pattern_length:
        seq = "".join(opponent_history[-pattern_length:])
        for i in range(len(opponent_history) - pattern_length):
            key = "".join(opponent_history[i:i + pattern_length])
            next_move = opponent_history[i + pattern_length]
            guess_map.setdefault(key, []).append(next_move)
        if seq in guess_map:
            prediction = Counter(guess_map[seq]).most_common(1)[0][0]
            pattern_move = beats_map[prediction]

    # Strategy 3: Cycle
    cycle_move = 'R'
    if len(opponent_history) >= 3:
        last_3 = opponent_history[-3:]
        if last_3 == ['R', 'P', 'S'] or last_3 == ['P', 'S', 'R'] or last_3 == ['S', 'R', 'P']:
            next_in_cycle = beats_map[opponent_history[-1]]
            cycle_move = beats_map[next_in_cycle]

    # Score each strategy
    if len(my_history) > 0 and len(opponent_history) > 1:
        last_opponent = opponent_history[-2]
        win_map = {'R': 'S', 'P': 'R', 'S': 'P'}
        for name, move in [('freq', freq_move), ('pattern', pattern_move), ('cycle', cycle_move)]:
            if win_map[move] == last_opponent:
                strategy_scores[name] += 1

    # Special detection
    if len(opponent_history) >= 5 and len(set(opponent_history[-5:])) == 1:
        return beats_map[opponent_history[-1]]

    if len(opponent_history) >= 6:
        last_six = opponent_history[-6:]
        if last_six[:3] == last_six[3:]:
            return beats_map[last_six[0]]

    if len(opponent_history) >= 1 and len(my_history) >= 1:
        if opponent_history[-1] == my_history[-1]:
            return beats_map[my_history[-1]]

    # Use best strategy
    best_strategy = max(strategy_scores, key=strategy_scores.get)
    move = {'freq': freq_move, 'pattern': pattern_move, 'cycle': cycle_move}[best_strategy]
    my_history.append(move)
    return move

# --- GUI Section ---
class RPSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors (AI)")
        self.root.geometry("400x350")
        self.root.configure(bg="#eef")

        self.player_history = []
        self.bot_history = []

        self.score = {'win': 0, 'loss': 0, 'draw': 0}

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Choose Your Move:", font=("Arial", 14)).pack(pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack()

        ttk.Button(button_frame, text="Rock", command=lambda: self.play("R")).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Paper", command=lambda: self.play("P")).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Scissors", command=lambda: self.play("S")).grid(row=0, column=2, padx=5)

        self.result_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=15)

        self.score_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.score_label.pack()

        ttk.Button(self.root, text="Reset", command=self.reset_game).pack(pady=10)

    def play(self, player_move):
        bot_move = adaptive_player(player_move)

        self.player_history.append(player_move)
        self.bot_history.append(bot_move)

        result = self.get_result(player_move, bot_move)
        self.update_score(result)
        self.result_label.config(text=f"You: {self.pretty(player_move)} | Bot: {self.pretty(bot_move)} | Result: {result}")
        self.score_label.config(text=f"Wins: {self.score['win']} | Losses: {self.score['loss']} | Draws: {self.score['draw']}")

    def get_result(self, player, bot):
        if player == bot:
            return "Draw"
        elif (player == 'R' and bot == 'S') or (player == 'P' and bot == 'R') or (player == 'S' and bot == 'P'):
            return "Win"
        else:
            return "Loss"

    def update_score(self, result):
        if result == "Win":
            self.score['win'] += 1
        elif result == "Loss":
            self.score['loss'] += 1
        else:
            self.score['draw'] += 1

    def reset_game(self):
        self.player_history.clear()
        self.bot_history.clear()
        for key in self.score:
            self.score[key] = 0
        self.result_label.config(text="")
        self.score_label.config(text="")

    def pretty(self, move):
        return {'R': "Rock", 'P': "Paper", 'S': "Scissors"}[move]

# --- Run GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = RPSGameGUI(root)
    root.mainloop()
