import os
import pygame.font

pygame.font.init()
lost_font = pygame.font.SysFont("comicsans", 60)
lost_label = lost_font.render("Game Over", 1, (0, 0, 0))
class Game:
    def __init__(self, board, window):
        self.image = None
        self.screen = None
        self.board = board
        self.window = window
        self.tileSize = self.window[0]//self.board.getSize()[1], self.window[1]//self.board.getSize()[0]
        self.loadImage()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.window)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    rightClick = pygame.mouse.get_pressed()[2]
                    self.handleClick(position, rightClick)
                self.draw()
            pygame.display.flip()
            if self.board.getWin() or self.board.getLost():
                pygame.time.delay(500)
                running = False
            pygame.display.flip()


    def draw(self):
        start = (0, 0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                tile = self.board.getTile((row, col))
                image = self.initImage(tile)
                self.screen.blit(image, start)
                start = start[0] + self.tileSize[0], start[1]
            start = 0, start[1] + self.tileSize[1]

    def loadImage(self):
        self.image = {}
        for file in os.listdir("assets"):
            if file.endswith("png"):
                image = pygame.image.load(r"assets/" + file)
                image = pygame.transform.scale(image, self.tileSize)
                self.image[file.split(".")[0]] = image

    def initImage(self, tile):
        string = None
        if tile.getClicked():
            string = "bomb-at-clicked-block" if tile.getHasBomb() else str(tile.getBoundary())
        else:
            string = "flag" if tile.getFlagged() else "empty-block"

        return self.image[string]

    def handleClick(self, position, rightClick):
        if self.board.getLost():
            return
        index = position[1] // self.tileSize[1], position[0] // self.tileSize[0]
        tile = self.board.getTile(index)
        self.board.handleClick(tile, rightClick)

    def reset(self):
        self.image = None
        self.screen = None
        self.loadImage()
