import pygame
import os

# initialize pygame and font
pygame.init()
pygame.font.init()

# define font
padding = 10
fontPath = os.path.join("asset", "font.ttf")
if not os.path.isfile(fontPath):
    raise FileNotFoundError(f"Font file not found: {fontPath}")

# load font
font = pygame.font.Font(fontPath, 30)
detailFont = pygame.font.Font(fontPath, 20)

# define screen
screenWidth = screenHeight = 750
screen = pygame.display.set_mode((screenWidth, screenHeight))
fps = 60
clock = pygame.time.Clock()

# game list
gameList = ["Minesweeper", "Tetris", "Space Invader", "Street Fighter"]
def drawMenu(games):
    for i in range(len(games)):
        menuLabel = font.render(games[i], True, "white")
        screen.blit(menuLabel, (screenWidth // 2 - menuLabel.get_width() // 2, 1.5 * logo.get_height() +
                                i * menuLabel.get_height() * 1.5))
running = True

# import images and logos
background = pygame.transform.scale(pygame.image.load(os.path.join("asset", "background.jpeg")),
                                    (screenWidth, screenHeight))
logo = pygame.transform.scale(pygame.image.load(os.path.join("asset", "logo.png")), (0.5 * 751, 0.5 * 299))

# render texts
authorLabel = detailFont.render("Made by: Hyunseok Cho, Jihwan Kim", True, "white")

def drawBackground(bg, lgo, lbl):
    screen.blit(bg, (0, 0))
    screen.blit(lgo, (screenWidth // 2 - logo.get_width() // 2, logo.get_height() // 2))
    screen.blit(lbl, (screenWidth - padding - authorLabel.get_width(), screenHeight - padding -
                              authorLabel.get_height()))
while running:
    clock.tick(fps)
    drawBackground(background, logo, authorLabel)
    drawMenu(gameList)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
