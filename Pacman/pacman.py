import pygame
import math
from board import boardList

pygame.init()

width, height = 750, 750
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont("comic-sans", 20)
level = boardList
color = "red"
pi = math.pi
def drawBoard():
    num1 = ((height-50)//32)
    num2 = (width//30)
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col] == 1:
                pygame.draw.circle(screen, "white", [col * num2 + (0.5 * num2), row * num1 +
                                                     (0.5 * num1)], 4)
            if level[row][col] == 2:
                pygame.draw.circle(screen, "white", [col * num2 + (0.5 * num2), row * num1 +
                                                     (0.5 * num1)], 10)
            if level[row][col] == 3:
                pygame.draw.line(screen, color, (col * num2 + (0.5 * num2), row * num1),
                                 (col * num2 + (0.5 * num2), row * num1 + num1), 1)
            if level[row][col] == 4:
                pygame.draw.line(screen, color, (col * num2, row * num1 + (0.5 * num1)),
                                 (col * num2 + num2, row * num1 + (0.5 * num1)), 1)
            if level[row][col] == 5:
                pygame.draw.arc(screen, color, [(col * num2 - (0.4 * num2)) - 2, (row * num1 + (0.5 * num1)),
                                                num2, num1], 0, pi/2, 1)
            if level[row][col] == 6:
                pygame.draw.arc(screen, color, [(col * num2 + (0.5 * num2)), (row * num1 + (0.5 * num1)),
                                                num2, num1], pi/2, pi, 1)
            if level[row][col] == 7:
                pygame.draw.arc(screen, color, [(col * num2 + (0.5 * num2))-0.5, (row * num1 - (0.4 * num1)-0.65),
                                                num2, num1], pi, 3 * pi/2, 1)
            if level[row][col] == 8:
                pygame.draw.arc(screen, color, [(col * num2 - (0.4 * num2)) - 2, (row * num1 - (0.4 * num1))-1,
                                                num2, num1], 3 * pi/2, 2*pi, 1)
            if level[row][col] == 9:
                pygame.draw.line(screen, "white", (col * num2, row * num1 + (0.5 * num1)),
                                 (col * num2 + num2, row * num1 + (0.5 * num1)), 1)

running = True
while running:
    clock.tick(fps)
    screen.fill("black")
    drawBoard()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()
