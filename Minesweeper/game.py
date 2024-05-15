import pygame
import os


class Game():
    def __init__(self, board, window):
        self.image = None
        self.screen = None
        self.board = board
        self.window = window
        self.tileSize = self.window[0]//self.board.getSize()[1], self.window[1]//self.board.getSize()[0]
        self.initImage()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.window)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        start = (0, 0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                image = self.image["empty-block"]
                self.screen.blit(image, start)
                start = start[0] + self.tileSize[0], start[1]
            start = 0, start[1] + self.tileSize[1]

    def initImage(self):
        self.image = {}
        for file in os.listdir("assets"):
            if file.endswith("png"):
                image = pygame.image.load(r"assets/" + file)
                image = pygame.transform.scale(image, self.tileSize)
                self.image[file.split(".")[0]] = image
