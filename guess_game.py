import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 500, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the Number")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 180, 0)
RED = (220, 50, 50)
BLUE = (50, 100, 220)
LIGHT_BLUE = (200, 220, 255)
ORANGE = (255, 150, 0)

FONT_TITLE = pygame.font.SysFont("arial", 36, bold=True)
FONT_TEXT = pygame.font.SysFont("arial", 24)
FONT_SMALL = pygame.font.SysFont("arial", 18)
FONT_INPUT = pygame.font.SysFont("arial", 28)

MIN_NUM, MAX_NUM = 1, 100


def new_game():
    return {
        "target": random.randint(MIN_NUM, MAX_NUM),
        "attempts": 0,
        "hint": "Enter a number and press Enter",
        "hint_color": BLACK,
        "won": False,
    }


def draw_button(surface, rect, text, color, text_color=WHITE):
    pygame.draw.rect(surface, color, rect, border_radius=8)
    label = FONT_TEXT.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)


def draw_centered(surface, text, font, color, y):
    label = font.render(text, True, color)
    rect = label.get_rect(center=(WIDTH // 2, y))
    surface.blit(label, rect)


def main():
    clock = pygame.time.Clock()
    game = new_game()
    user_input = ""
    input_active = True

    input_rect = pygame.Rect(WIDTH // 2 - 80, 200, 160, 45)
    restart_rect = pygame.Rect(WIDTH // 2 - 50, 320, 100, 40)

    while True:
        WIN.fill(LIGHT_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game["won"]:
                if event.key == pygame.K_RETURN:
                    if user_input.isdigit():
                        guess = int(user_input)
                        game["attempts"] += 1
                        if guess < game["target"]:
                            game["hint"] = f"{guess} is too low!"
                            game["hint_color"] = BLUE
                        elif guess > game["target"]:
                            game["hint"] = f"{guess} is too high!"
                            game["hint_color"] = ORANGE
                        else:
                            game["hint"] = f"Correct! It was {game['target']} ({game['attempts']} tries)"
                            game["hint_color"] = GREEN
                            game["won"] = True
                        user_input = ""
                    else:
                        game["hint"] = "Please enter a valid number"
                        game["hint_color"] = RED
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isdigit() and len(user_input) < 3:
                    user_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    game = new_game()
                    user_input = ""

        draw_centered(WIN, "Guess the Number", FONT_TITLE, BLACK, 40)
        draw_centered(WIN, f"( between {MIN_NUM} and {MAX_NUM} )", FONT_SMALL, DARK_GRAY, 75)

        color = GRAY if game["won"] else WHITE
        pygame.draw.rect(WIN, color, input_rect, border_radius=6)
        pygame.draw.rect(WIN, DARK_GRAY, input_rect, 2, border_radius=6)

        input_label = FONT_INPUT.render(user_input if user_input else "___", True, BLACK)
        WIN.blit(input_label, input_label.get_rect(center=input_rect.center))

        if game["attempts"] > 0 or game["won"]:
            draw_centered(WIN, game["hint"], FONT_TEXT, game["hint_color"], 270)
        else:
            draw_centered(WIN, "Enter a number and press Enter", FONT_SMALL, DARK_GRAY, 270)

        draw_centered(WIN, f"Attempts: {game['attempts']}", FONT_SMALL, DARK_GRAY, 300)

        draw_button(WIN, restart_rect, "Restart", RED)

        if game["won"]:
            s = pygame.Surface((WIDTH, HEIGHT - 320))
            s.set_alpha(100)
            s.fill(GREEN)
            WIN.blit(s, (0, 320))

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
