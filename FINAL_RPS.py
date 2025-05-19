import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors - AI Battle")

# Fonts
font = pygame.font.SysFont("Arial", 32)
emoji_font = pygame.font.SysFont("Segoe UI Emoji", 80)
button_font = pygame.font.SysFont("Arial", 28)

# Colors
WHITE = (255, 255, 255)
GRAY = (210, 210, 210)
BLACK = (0, 0, 0)
BLUE = (173, 216, 230)

# Emoji icons
emoji_dict = {"R": "🪨", "P": "📄", "S": "✂️"}

# Bots
def random_bot(_): return random.choice(["R", "P", "S"])
def repeat_rock_bot(_): return "R"
def cycle_bot(history): return ["R", "P", "S"][len(history) % 3]
def copy_last_move_bot(history): return random.choice(["R", "P", "S"]) if not history else history[-1]

bot_options = {
    "Random Bot": random_bot,
    "Rock Repeater": repeat_rock_bot,
    "Cycle Bot": cycle_bot,
    "Copycat Bot": copy_last_move_bot
}

def beats(a, b): return (a == 'R' and b == 'S') or (a == 'P' and b == 'R') or (a == 'S' and b == 'P')

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = button_font.render(text, True, BLACK)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

def draw_emoji_button(symbol, x, y):
    emoji = emoji_font.render(emoji_dict[symbol], True, BLACK)
    rect = emoji.get_rect(center=(x, y))
    screen.blit(emoji, rect)
    return rect

def game_loop(bot_func):
    history = []
    result = ""
    player_move = None
    bot_move = None

    while True:
        screen.fill(WHITE)
        title = font.render("Choose your move:", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Draw emoji buttons
        rock_rect = draw_emoji_button("R", 200, 250)
        paper_rect = draw_emoji_button("P", 400, 250)
        scissors_rect = draw_emoji_button("S", 600, 250)

        # Result display
        if result:
            result_text = font.render(result, True, BLACK)
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 400))

        # Buttons
        back_btn = draw_button("Back", 10, 10, 100, 40, GRAY)
        exit_btn = draw_button("Exit", WIDTH - 110, 10, 100, 40, GRAY)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos): return
                if exit_btn.collidepoint(event.pos): pygame.quit(); sys.exit()

                if rock_rect.collidepoint(event.pos): player_move = "R"
                elif paper_rect.collidepoint(event.pos): player_move = "P"
                elif scissors_rect.collidepoint(event.pos): player_move = "S"

                if player_move:
                    bot_move = bot_func(history)
                    history.append(bot_move)

                    if player_move == bot_move:
                        result = "Draw! 🤝"
                    elif beats(player_move, bot_move):
                        result = "You Win! 🎉"
                    else:
                        result = "You Lose! 😢"
                    result += f"  You: {emoji_dict[player_move]} vs Bot: {emoji_dict[bot_move]}"
                    player_move = None

def menu():
    while True:
        screen.fill(WHITE)
        title = font.render("Select Your Opponent AI", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        y = 150
        buttons = []
        for name in bot_options:
            btn = draw_button(name, 250, y, 300, 50, BLUE)
            buttons.append((btn, bot_options[name]))
            y += 70

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, bot_func in buttons:
                    if rect.collidepoint(event.pos):
                        game_loop(bot_func)

# Run the menu
menu()
