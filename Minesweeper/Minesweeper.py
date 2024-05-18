from game import Game
from board import Board
import pygame.font
import time

pygame.font.init()

size = (9, 9)
prob = 0.5
board = Board(size, prob)
width, height = 750, 750
screen = pygame.display.set_mode((width, height))
menu_font = pygame.font.SysFont("comicsans", 40)

def main_menu():
    clock = pygame.time.Clock()
    running = True

    # Blinking message
    textVisible = True
    lastVisibleTime = time.time()
    blinkInterval = 0.5

    while running:
        screen.fill((200, 200, 200))
        currentTime = time.time()
        if currentTime - lastVisibleTime >= blinkInterval:
            textVisible = not textVisible
            lastVisibleTime = currentTime
        if textVisible:
            menu_label = menu_font.render("Press any key to begin", 1, (0, 0, 0))
            screen.blit(menu_label, (width / 2 - menu_label.get_width() / 2, height / 2 - menu_label.get_height() / 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game.run()

        clock.tick(60)
    pygame.quit()

game = Game(board, (width, height), main_menu)
main_menu()
