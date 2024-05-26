from game import Game
from board import Board
import pygame.font
import time
import os
import sys
from pathlib import Path
import importlib.util

pygame.font.init()

size = (9, 9)
prob = 0.4
board = Board(size, prob)
width, height = 750, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mine Sweeper")

currPath = Path(os.getcwd())
fontPath = os.path.join(currPath.parent, "asset", "font.ttf")

menu_font = pygame.font.Font(fontPath, 40)
game = Game(board, (width, height))

menu_label = menu_font.render("Press any key to begin", 1, (0, 0, 0))
won_label = menu_font.render("You win!", 1, (0, 0, 0))
lost_label = menu_font.render("GAME OVER", 1, (0, 0, 0))

def main_menu():
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

    # Blinking message
    textVisible = True
    lastVisibleTime = time.time()
    blinkInterval = 0.5

    running = True
    while running:
        screen.fill((200, 200, 200))
        currentTime = time.time()
        if board.getLost():
            screen.blit(lost_label, (width // 2 - lost_label.get_width() // 2, height // 3))
        if board.getWin():
            screen.blit(won_label, (width // 2 - lost_label.get_width() // 2, height // 3))
        if currentTime - lastVisibleTime >= blinkInterval:
            textVisible = not textVisible
            lastVisibleTime = currentTime
        if textVisible:
            screen.blit(menu_label, (width / 2 - menu_label.get_width() / 2,
                                     height / 2 - menu_label.get_height() / 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    returnMenu()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                game.reset()
                board.reset()
                game.run()

    pygame.quit()
main_menu()
