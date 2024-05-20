from game import Game
from board import Board
import pygame.font
import time

pygame.font.init()

size = (9, 9)
prob = 0.4
board = Board(size, prob)
width, height = 750, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper")
menu_font = pygame.font.SysFont("comicsans", 40)
game = Game(board, (width, height))

menu_label = menu_font.render("Press any key to begin", 1, (0, 0, 0))
won_label = menu_font.render("You win!", 1, (0,0,0))
lost_label = menu_font.render("GAME OVER", 1, (0,0,0))

def main_menu():
    running = True

    # Blinking message
    textVisible = True
    lastVisibleTime = time.time()
    blinkInterval = 0.5

    while running:
        screen.fill((200, 200, 200))
        currentTime = time.time()
        if board.getLost():
            screen.blit(lost_label, (width//2 - lost_label.get_width()//2, height//3))
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
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                game.reset()
                board.reset()
                game.run()

    pygame.quit()

main_menu()
