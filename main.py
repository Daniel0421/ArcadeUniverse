import pygame
import os

# initialize pygame and font
pygame.init()
pygame.font.init()
pygame.display.set_caption("Arcade Universe")

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


gameList = sorted(getGameList())
optionList = ['OPTIONS', 'QUIT']

def drawBackground(bg, lgo, lbl):
    screen.blit(bg, (0, 0))
    screen.blit(lgo, (screenWidth // 2 - logo.get_width() // 2, logo.get_height() // 2))
    screen.blit(lbl, (screenWidth // 2 - padding - authorLabel.get_width() // 2, screenHeight - padding -
                      authorLabel.get_height()))


class Game_menu:
    def __init__(self, width, height, games):
        self.screenWidth = width
        self.screenHeight = height
        self.rectWidth = width * 0.8
        self.rectHeight = height * 0.3
        self.rectX = width // 2 - self.rectWidth // 2
        self.rectY = height // 2 - self.rectHeight // 2
        self.padding = padding
        self.gameList = games

    def drawGameOuter(self, screenSize):
        pygame.draw.rect(screenSize, "white", pygame.Rect(self.rectX, self.rectY, self.rectWidth,
                                                          self.rectHeight), 2, border_radius=10)

    def drawGameInner(self, screenSize):
        newY = self.rectY + self.padding
        newHeight = self.rectHeight - 2 * self.padding
        newWidth = (self.rectWidth - (len(self.gameList) + 1) * self.padding) / (len(self.gameList))
        midpointY = newHeight // 2

        # inserting button and image
        for imageTile in range(len(self.gameList)):
            # drawing game tile
            newX = self.rectX + self.padding + imageTile * (newWidth + self.padding)
            pygame.draw.rect(screenSize, "white", pygame.Rect(newX, newY, newWidth, newHeight), 2,
                             border_radius=10)

            # insert image
            imagePath = os.path.join(self.gameList[imageTile], "assets", "logo.png")
            imageLoad = pygame.image.load(imagePath)
            factor = (midpointY - 2 * self.padding) / imageLoad.get_height()
            imageScale = pygame.transform.scale_by(imageLoad, factor)
            imageCenter = newWidth // 2 - imageScale.get_width() // 2
            screen.blit(imageScale, (newX + imageCenter, newY + 2 * self.padding))

            # insert title
            titleLabel = font.render(gameList[imageTile].upper(), True, "white")
            titleCenter = newWidth // 2 - titleLabel.get_width() // 2
            titleCenterY = newY + 1.5 * midpointY - titleLabel.get_height() // 2
            if titleLabel.get_width() >= newWidth:
                title = gameList[imageTile].split()
                label = []
                for word in title:
                    label.append(word)
                for i in range(len(label)):
                    titleLabel = font.render(label[i].upper(), True, "white")
                    titleCenter = newWidth // 2 - titleLabel.get_width() // 2
                    titleCenterY = newY + 1.5 * midpointY - titleLabel.get_height()
                    screen.blit(titleLabel, (newX + titleCenter, titleCenterY + i * titleLabel.get_height()))
            else:
                screen.blit(titleLabel, (newX + titleCenter, titleCenterY))

class Option_menu(Game_menu):
    def __init__(self, options):
        super().__init__(screenWidth, screenHeight, gameList)
        self.options = optionList
        self.startY = self.rectY + self.padding + self.rectHeight


    def drawBox(self):
        for i in range(len(self.options)):

            # draw box
            width = (self.rectWidth - self.padding) // len(self.options)
            startX = self.rectX + i * (width + self.padding)
            pygame.draw.rect(screen, "white", pygame.Rect(startX, self.startY, width, 50), 2, border_radius=10)

            # draw text
            optionLabel = font.render(self.options[i], True, "white")
            optionX = startX + width // 2 - optionLabel.get_width() // 2
            optionY = self.startY + 25 - optionLabel.get_height() // 2
            screen.blit(optionLabel, (optionX, optionY))


game = Game_menu(screenWidth, screenHeight, gameList)
option = Option_menu(optionList)

running = True
while running:
    clock.tick(fps)
    drawBackground(background, logo, authorLabel)
    game.drawGameOuter(screen)
    game.drawGameInner(screen)
    option.drawBox()

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
