import pygame
import sys
import os
from pathlib import Path
from colors import Colors
from game import Game
import importlib.util

pygame.init()

# initialize font
currPath = Path(os.getcwd())
fontPath = os.path.join(currPath.parent, "asset", "font.ttf")

title_font = pygame.font.Font(fontPath, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
start_surface = title_font.render("Press any key to start", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((750, 750))
pygame.display.set_caption("TETRIS")

clock = pygame.time.Clock()

game = Game()

# game state
HOME, PLAYING = 'HOME', 'PLAYING'
game_state = HOME

GAME_UPDATE = pygame.USEREVENT
BLINK_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(GAME_UPDATE, 200)
pygame.time.set_timer(BLINK_UPDATE, 500)
pygame.key.set_repeat(100, 200)

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

show_message = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state == HOME:
                game_state = PLAYING
            if game.game_over:
                game.game_over = False
                game.reset()
            else:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game.move_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game.move_right()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.rotate()
                if event.key == pygame.K_ESCAPE:
                    returnMenu()
        if event.type == GAME_UPDATE and not game.game_over and game_state == PLAYING:
            game.move_down()
        if event.type == BLINK_UPDATE:
            show_message = not show_message

    # Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (349, 20, 50, 50))
    screen.blit(next_surface, (363, 180, 50, 50))

    if game_state == HOME and show_message:
        screen.blit(start_surface, (313, 450+2*game_over_surface.get_height(), 50, 50))
    elif game.game_over:
        screen.blit(game_over_surface, (320, 450, 50, 50))
        if show_message:
            screen.blit(start_surface, (313, 450+2*game_over_surface.get_height(), 50, 50))
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface,
                score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)
    pygame.display.update()
    clock.tick(60)
