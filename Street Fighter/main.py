import sys
import pygame
from fighter import Fighter
from pathlib import Path
import os
import importlib.util

pygame.init()

Screen_w = 1000
Screen_h = 600

screen = pygame.display.set_mode((Screen_w, Screen_h))
pygame.display.set_caption("Street Fighter")

Clock = pygame.time.Clock()
FPS = 60

intro_cnt = 3  # Countdown for the start of the game
last_cnt_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
round_over_cooldown = 2000
Game_run = False
show_controls = True  # New state for showing controls

warrior_size = 162
warrior_scale = 4
warrior_offset = [72, 56]
warrior_data = [warrior_size, warrior_scale, warrior_offset]
wizard_size = 250
wizard_scale = 3
wizard_offset = [112, 107]
wizard_data = [wizard_size, wizard_scale, wizard_offset]

bg = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

WARRIOR_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_STEPS = [8, 8, 1, 8, 8, 3, 7]

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

currPath = Path(os.getcwd())
fontPath = os.path.join(currPath.parent, "asset", "font.ttf")

title_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
cnt_font = pygame.font.Font(fontPath, 80)
score_font = pygame.font.Font(fontPath, 30)
controls_font = pygame.font.Font(fontPath, 30)
start_font = pygame.font.Font(fontPath, 50)

def draw_text(text, font, text_col, x, y, outline_col=None):
    if outline_col:
        # Drawing outline by rendering text multiple times
        img = font.render(text, True, outline_col)
        screen.blit(img, (x - 2, y - 2))
        screen.blit(img, (x + 2, y - 2))
        screen.blit(img, (x - 2, y + 2))
        screen.blit(img, (x + 2, y + 2))
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    scale_bg = pygame.transform.scale(bg, (Screen_w, Screen_h))
    screen.blit(scale_bg, (0, 0))

def draw_hb(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, BLACK, (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

def show_controls_screen():
    draw_bg()
    draw_text("1 vs 1 Fighting Game", title_font, RED, Screen_w // 2 - 300, 20, outline_col=BLACK)

    # Player 1 controls
    draw_text("Player 1:", controls_font, BLACK, 20, 120)
    draw_text("A - Move Left", controls_font, BLACK, 20, 150)
    draw_text("D - Move Right", controls_font, BLACK, 20, 200)
    draw_text("W - Jump", controls_font, BLACK, 20, 240)
    draw_text("R/T - Attack", controls_font, BLACK, 20, 280)
    # Player 2 controls
    draw_text("Player 2:", controls_font, BLACK, Screen_w - 700, 120)
    draw_text("Left Arrow - Move Left", controls_font, BLACK, Screen_w - 700, 150)
    draw_text("Right Arrow - Move Right", controls_font, BLACK, Screen_w - 700, 200)
    draw_text("Up Arrow - Jump", controls_font, BLACK, Screen_w - 700, 240)
    draw_text(",/. - Attack", controls_font, BLACK, Screen_w - 700, 280)
    # Blinking "Press Enter to Start" text
    if pygame.time.get_ticks() % 1000 < 500:
        draw_text("Press Enter to Start", start_font, WHITE, Screen_w // 2 - 300, Screen_h - 200)

fighter_1 = Fighter(1, 200, 310, False, warrior_data, warrior_sheet, WARRIOR_STEPS)
fighter_2 = Fighter(2, 700, 310, True, wizard_data, wizard_sheet, WIZARD_STEPS)

def returnMenu():
    curr_dir = Path(os.getcwd())
    home_dir = curr_dir.parent
    os.chdir(home_dir)  # Change to the directory of main.py

    # Reload the main module to reset its state
    module_name = "main"
    if module_name in sys.modules:
        del sys.modules[module_name]  # Remove the existing module from sys.modules

    spec = importlib.util.spec_from_file_location(module_name, home_dir / "main.py")
    newModule = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = newModule
    spec.loader.exec_module(newModule)

run = True

while run:
    Clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and show_controls:
                show_controls = False
                Game_run = True
                intro_cnt = 3  # Start countdown
            if event.key == pygame.K_ESCAPE:
                returnMenu()

    if show_controls:
        show_controls_screen()
    elif not Game_run:
        draw_bg()

    elif Game_run:
        draw_bg()

        draw_hb(fighter_1.health, 20, 20)
        draw_hb(fighter_2.health, 580, 20)

        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        if intro_cnt > 0:
            draw_text(str(intro_cnt), cnt_font, RED, Screen_w // 2 - 20, Screen_h / 3)
            if (pygame.time.get_ticks() - last_cnt_update) >= 1000:
                intro_cnt -= 1
                last_cnt_update = pygame.time.get_ticks()
        else:
            fighter_1.move(Screen_w, Screen_h, screen, fighter_2, round_over)
            fighter_2.move(Screen_w, Screen_h, screen, fighter_1, round_over)

        fighter_1.update()
        fighter_2.update()

        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
                round_over = False
                intro_cnt = 3
                fighter_1 = Fighter(1, 200, 310, False, warrior_data, warrior_sheet, WARRIOR_STEPS)
                fighter_2 = Fighter(2, 700, 310, True, wizard_data, wizard_sheet, WIZARD_STEPS)

    pygame.display.update()

pygame.quit()
