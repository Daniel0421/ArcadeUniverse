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

menuList = [False] * (len(gameList) + len(optionList))
menuList[0] = True

# [['Mine Sweeper', 'Space Invader', 'Street Fighter', 'Tetris'],
# ['OPTIONS', 'QUIT']]

def drawBackground(bg, lgo, lbl, screenSize, width, height, pdg):
    rectWidth = width * 0.8
    rectHeight = height * 0.3
    rectX = width // 2 - rectWidth // 2
    rectY = height // 2 - rectHeight // 2
    screen.blit(bg, (0, 0))
    screen.blit(lgo, (width // 2 - lgo.get_width() // 2, lgo.get_height() // 2))
    screen.blit(lbl, (width // 2 - pdg - lbl.get_width() // 2, height - pdg -
                      lbl.get_height()))
    pygame.draw.rect(screenSize, "white", pygame.Rect(rectX, rectY, rectWidth,
                                                      rectHeight), 2, border_radius=10)

class Navigate:
    def __init__(self, menu):
        self.menulist = menu

    def reset(self):
        self.menulist = [False] * len(self.menulist)

    def update(self, events):
        newIndex = None
        length = len(self.menulist)
        currentIndex = self.menulist.index(True)
        if events.key == pygame.K_d or events.key == pygame.K_RIGHT:
            newIndex = (currentIndex + 1) % length
        if events.key == pygame.K_a or events.key == pygame.K_LEFT:
            newIndex = (currentIndex - 1 + length) % length

        if newIndex is not None:
            self.reset()
            self.menulist[newIndex] = True
        return self.menulist

class Game_menu:
    def __init__(self, width, height, games, pdg, opn):
        self.screenWidth = width
        self.screenHeight = height
        self.rectWidth = width * 0.8
        self.rectHeight = height * 0.3
        self.rectX = width // 2 - self.rectWidth // 2
        self.rectY = height // 2 - self.rectHeight // 2
        self.padding = pdg
        self.gameList = games

        self.newY = self.rectY + self.padding
        self.newHeight = self.rectHeight - 2 * self.padding
        self.newWidth = (self.rectWidth - (len(self.gameList) + 1) * self.padding) / (len(self.gameList))
        self.midpointY = self.newHeight // 2

        self.option = opn
        self.startY = self.rectY + self.padding + self.rectHeight

    def drawGameButton(self, screenSize, imageTile, color, thickness):
        # drawing game tile
        newX = self.rectX + self.padding + imageTile * (self.newWidth + self.padding)
        pygame.draw.rect(screenSize, color, pygame.Rect(newX, self.newY, self.newWidth, self.newHeight), thickness,
                         border_radius=10)

        # insert image
        imagePath = os.path.join(self.gameList[imageTile], "assets", "logo.png")
        imageLoad = pygame.image.load(imagePath)
        factor = (self.midpointY - 2 * self.padding) / imageLoad.get_height()
        imageScale = pygame.transform.scale_by(imageLoad, factor)
        imageCenter = self.newWidth // 2 - imageScale.get_width() // 2
        screen.blit(imageScale, (newX + imageCenter, self.newY + 2 * self.padding))

        # insert title
        titleLabel = font.render(gameList[imageTile].upper(), True, color)
        titleCenter = self.newWidth // 2 - titleLabel.get_width() // 2
        titleCenterY = self.newY + 1.5 * self.midpointY - titleLabel.get_height() // 2
        if titleLabel.get_width() >= self.newWidth:
            title = gameList[imageTile].split()
            label = []
            for word in title:
                label.append(word)
            for i in range(len(label)):
                titleLabel = font.render(label[i].upper(), True, color)
                titleCenter = self.newWidth // 2 - titleLabel.get_width() // 2
                titleCenterY = self.newY + 1.5 * self.midpointY - titleLabel.get_height()
                screen.blit(titleLabel, (newX + titleCenter, titleCenterY + i * titleLabel.get_height()))
        else:
            screen.blit(titleLabel, (newX + titleCenter, titleCenterY))

    def drawOptionButton(self, i, color, thickness):
        # draw box
        width = (self.rectWidth - self.padding) // len(self.option)
        startX = self.rectX + i * (width + self.padding)
        pygame.draw.rect(screen, color, pygame.Rect(startX, self.startY, width, 50), thickness, border_radius=10)

        # draw text
        optionLabel = font.render(self.option[i], True, color)
        optionX = startX + width // 2 - optionLabel.get_width() // 2
        optionY = self.startY + 25 - optionLabel.get_height() // 2
        screen.blit(optionLabel, (optionX, optionY))

    def run(self, screenSize,):
        hoverColor = "green"
        baseColor = "white"
        baseThickness = 2
        hoverThickness = 4

        # draw game tiles
        for imageTile in range(len(self.gameList)):
            if menuList[imageTile]:
                self.drawGameButton(screenSize, imageTile, hoverColor, hoverThickness)
            else:
                self.drawGameButton(screenSize, imageTile, baseColor, baseThickness)
        # draw option tiles
        for i in range(len(self.option)):
            if menuList[len(self.gameList) + i]:
                self.drawOptionButton(i, hoverColor, hoverThickness)
            else:
                self.drawOptionButton(i, baseColor, baseThickness)

game = Game_menu(screenWidth, screenHeight, gameList, padding, optionList)
navigate = Navigate(menuList)
running = True
while running:
    clock.tick(fps)
    drawBackground(background, logo, authorLabel, screen, screenWidth, screenHeight, padding)
    game.run(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            menuList = navigate.update(event)
    pygame.display.flip()
pygame.quit()
