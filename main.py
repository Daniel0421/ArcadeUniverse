import pygame
import os

# initialize pygame and font
pygame.init()
pygame.font.init()

# initialize constants
padding = 10
screenWidth = screenHeight = 750
fps = 60
bigFont = 30
smallFont = 20

# set paths
backgroundPath = os.path.join("asset", "background.jpeg")
logoPath = os.path.join("asset", "logo.png")
fontPath = os.path.join("asset", "font.ttf")

# raise errors
if not os.path.isfile(fontPath):
    raise FileNotFoundError(f"Font file not found: {fontPath}")
if not os.path.isfile(backgroundPath):
    raise FileNotFoundError(f"Background file not found: {backgroundPath}")
if not os.path.isfile(logoPath):
    raise FileNotFoundError(f"Logo file not found: {logoPath}")

# load font
font = pygame.font.Font(fontPath, bigFont)
detailFont = pygame.font.Font(fontPath, smallFont)

# define screen
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

# import images and logos
getBackground = pygame.image.load(backgroundPath)
background = pygame.transform.scale(getBackground, (screenWidth, screenHeight))
getLogo = pygame.image.load(logoPath)
logo = pygame.transform.scale(getLogo, (0.5 * getLogo.get_width(), 0.5 * getLogo.get_height()))

# render texts
authorLabel = detailFont.render("Made by: Hyunseok Cho, Jihwan Kim", True, "white")


# game list
def getGameList():
    games = []
    currentDirectory = os.getcwd()
    for entry in os.listdir(currentDirectory):
        if os.path.isdir(os.path.join(currentDirectory, entry)) and entry[0].isupper() and not entry.startswith("P"):
            games.append(entry)
    return games


gameList = getGameList()


def drawMenu(games):
    for i in range(len(games)):
        menuLabel = font.render(games[i], True, "white")
        screen.blit(menuLabel, (screenWidth // 2 - menuLabel.get_width() // 2, 2 * logo.get_height() +
                                i * menuLabel.get_height() * 1.5))


def drawBackground(bg, lgo, lbl):
    screen.blit(bg, (0, 0))
    screen.blit(lgo, (screenWidth // 2 - logo.get_width() // 2, logo.get_height() // 2))
    screen.blit(lbl, (screenWidth - padding - authorLabel.get_width(), screenHeight - padding -
                      authorLabel.get_height()))


class Game_menu:
    def __init__(self, width, height, games):
        self.screenWidth = width
        self.screenHeight = height
        self.rectWidth = width * 0.8
        self.rectHeight = height * 0.3
        self.rectX = width // 2 - self.rectWidth // 2
        self.rectY = height // 2 - self.rectHeight // 2
        self.padding = 5
        self.gameList = games

    def drawGameOuter(self, screenSize):
        pygame.draw.rect(screenSize, "white", pygame.Rect(self.rectX, self.rectY, self.rectWidth,
                                                          self.rectHeight), 2)

    def drawGameInner(self, screenSize):
        newY = self.rectY + self.padding
        newHeight = self.rectHeight - 2 * self.padding
        newWidth = (self.rectWidth - (len(self.gameList) + 1) * self.padding) / (len(self.gameList))

        for gameTile in range(len(self.gameList)):
            # drawing game tile
            newX = self.rectX + self.padding + gameTile * (newWidth + self.padding)
            pygame.draw.rect(screenSize, "white", pygame.Rect(newX, newY, newWidth, newHeight), 2)

            # insert game title and image
            midpointY = newHeight // 2
            pygame.draw.rect(screenSize, "white", pygame.Rect(newX, newY, newWidth, midpointY))

game = Game_menu(screenWidth, screenHeight, gameList)

running = True
while running:
    clock.tick(fps)
    drawBackground(background, logo, authorLabel)
    # drawMenu(gameList)
    game.drawGameOuter(screen)
    game.drawGameInner(screen)
    pygame.display.flip()
    print(gameList)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
