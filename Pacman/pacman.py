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
directionCommand = 0
playerVelocity = 2

for i in range(1, 3):
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
    frame = (counter // 6) % len(playerImg)
    # 0 RIGHT, 1 LEFT, 2 UP, 3 DOWN
    if direction == 0:
        screen.blit(playerImg[frame], (playerX, playerY))
    if direction == 1:
        screen.blit(pygame.transform.flip(playerImg[frame], True, False), (playerX, playerY))
    if direction == 2:
        screen.blit(pygame.transform.rotate(playerImg[frame], 90), (playerX, playerY))
    if direction == 3:
        screen.blit(pygame.transform.rotate(playerImg[frame], 270), (playerX, playerY))

def checkPosition(centerx, centery):
    turn = [False, False, False, False]    # right, left, up, down
    tileHeight = (height - 50) // 32
    tileWidth = width // 30
    padding = 15

    # check for collision
    if centerx // tileWidth < 29:
        if direction == 0:
            if level[centery // tileHeight][(centerx - padding) // tileWidth] < 3:
                turn[1] = True
        if direction == 1:
            if level[centery // tileHeight][(centerx + padding) // tileWidth] < 3:
                turn[0] = True
        if direction == 2:
            if level[(centery + padding) // tileHeight][centerx // tileWidth] < 3:
                turn[3] = True
        if direction == 3:
            if level[(centery - padding) // tileHeight][centerx // tileWidth] < 3:
                turn[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % tileWidth <= 18:
                if level[(centery + padding) // tileHeight][centerx // tileWidth] < 3:
                    turn[3] = True
                if level[(centery - padding) // tileHeight][centerx // tileWidth] < 3:
                    turn[2] = True
            if 12 <= centerx % tileHeight <= 18:
                if level[centery // tileHeight][(centerx - tileWidth) // tileWidth] < 3:
                    turn[1] = True
                if level[centery // tileHeight][(centerx - tileWidth) // tileWidth] < 3:
                    turn[0] = True

        if direction == 0 or direction == 1:
            if 12 <= centerx % tileWidth <= 18:
                if level[(centery + tileHeight) // tileHeight][centerx // tileWidth] < 3:
                    turn[3] = True
                if level[(centery - tileHeight) // tileHeight][centerx // tileWidth] < 3:
                    turn[2] = True
            if 12 <= centery % tileHeight <= 18:
                if level[centery // tileHeight][(centerx - padding) // tileWidth] < 3:
                    turn[1] = True
                if level[centery // tileHeight][(centerx - padding) // tileWidth] < 3:
                    turn[0] = True
    else:
        turn[0], turn[1] = True, True

    return turn

def movePlayer(playx, playy):
    if direction == 0 and validTurn[0]:
        playx += playerVelocity
    elif direction == 1 and validTurn[1]:
        playx -= playerVelocity
    if direction == 2 and validTurn[2]:
        playy -= playerVelocity
    elif direction == 3 and validTurn[3]:
        playy += playerVelocity
    return playx, playy

running = True
while running:
    clock.tick(fps)
    if counter < fps/3:
        counter += 1
        if counter >= 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    screen.fill("black")
    drawBoard()
    drawPlayer()
    centerX = playerX + playerImg[0].get_width() // 2 + 1
    centerY = int(playerY) + playerImg[0].get_height() // 2 + 1
    validTurn = checkPosition(centerX, centerY)
    playerX, playerY = movePlayer(playerX, playerY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                directionCommand = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                directionCommand = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                directionCommand = 2
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                directionCommand = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d and directionCommand == 0:
                directionCommand = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a and directionCommand == 1:
                directionCommand = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w and directionCommand == 2:
                directionCommand = 2
            if event.key == pygame.K_DOWN or event.key == pygame.K_s and directionCommand == 3:
                directionCommand = 3

        for i in range(4):
            if directionCommand == i and validTurn[i]:
                direction = i

        if playerX > width:
            playerX = -47
        elif playerX < -50:
            playerX = width - 3

    pygame.display.flip()
pygame.quit()
