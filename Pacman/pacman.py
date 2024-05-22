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
color = "blue"
pi = math.pi
playerImg = []
flicker = False

for i in range(1,5):
    playerImg.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (35, 35)))
playerX = width//2 - playerImg[0].get_width()//2
playerY = height//2 + 3.5 * playerImg[0].get_height()
direction = 0
counter = 0
def drawBoard():
    num1 = ((height-50)//32)
    num2 = (width//30)
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col] == 1:
                pygame.draw.circle(screen, "white", [col * num2 + (0.5 * num2), row * num1 +
                                                     (0.5 * num1)], 4)
            if level[row][col] == 2 and not flicker:
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

def drawPlayer():
    # 0 RIGHT, 1 LEFT, 2 UP, 3 DOWN
    if direction == 0:
        screen.blit(playerImg[counter//5], (playerX, playerY))
    if direction == 1:
        screen.blit(pygame.transform.flip(playerImg[counter//5], True, False), (playerX, playerY))
    if direction == 2:
        screen.blit(pygame.transform.rotate(playerImg[counter//5], 90), (playerX, playerY))
    if direction == 3:
        screen.blit(pygame.transform.rotate(playerImg[counter//5], 270), (playerX, playerY))

running = True
while running:
    clock.tick(fps)
    if counter < fps/3-1:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    screen.fill("black")
    drawBoard()
    drawPlayer()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                direction = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                direction = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                direction = 2
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                direction = 3

    pygame.display.flip()
pygame.quit()
