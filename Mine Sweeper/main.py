import os
import pygame.font
from pathlib import Path
from board import Board
import importlib.util
import sys
import time

pygame.font.init()
currPath = Path(os.getcwd())
fontPath = os.path.join(currPath.parent, "asset", "font.ttf")

menu_font = pygame.font.Font(fontPath, 60)

size = (9, 9)
prob = 0.4
board = Board(size, prob)
width, height = 750, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mine Sweeper")

currPath = Path(os.getcwd())
fontPath = os.path.join(currPath.parent, "asset", "font.ttf")

class Game:
    def __init__(self, tile, window, font):
        self.image = None
        self.screen = None
        self.board = tile
        self.window = window
        self.tileSize = self.window[0]//self.board.getSize()[1], self.window[1]//self.board.getSize()[0]
        self.loadImage()
        self.font = font
        self.gameStarted = False
        self.gameOver = False

    @staticmethod
    def returnMenu():
        curr_dir = Path(os.getcwd())
        home_dir = curr_dir.parent
        os.chdir(home_dir)  # Change to the directory of main.py

        # Reload the main module to reset its state
        module_name = "main"
        if module_name in sys.modules:
            del sys.modules[module_name]  # Remove the existing module from sys.modules

        spec = importlib.util.spec_from_file_location(module_name, home_dir / "main.py")
        newModule = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = newModule
        spec.loader.exec_module(newModule)

    def resetGame(self):
        self.board = Board(size, prob)
        self.gameStarted = False
        self.gameOver = False
        self.loadImage()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.window)
        clock = pygame.time.Clock()

        textVisible = True
        blinkInterval = 0.5
        lastVisibleTime = time.time()

        menu_label = self.font.render("Press any key to begin", 1, (0, 0, 0))
        won_label = self.font.render("You win!", 1, (0, 0, 0))
        lost_label = self.font.render("GAME OVER", 1, (0, 0, 0))
        restart_label = self.font.render("Press any key to start again", 1, (0, 0, 0))

        running = True

        while running:
            screen.fill((200, 200, 200))
            currentTime = time.time()

            if self.board.getLost():
                self.draw()
                screen.blit(lost_label, (width // 2 - lost_label.get_width() // 2, height // 3))
                self.gameOver = True
            elif self.board.getWin():
                screen.blit(won_label, (width // 2 - won_label.get_width() // 2, height // 3))
                self.gameOver = True
            else:
                if not self.gameStarted:
                    if currentTime - lastVisibleTime >= blinkInterval:
                        textVisible = not textVisible
                        lastVisibleTime = currentTime
                    if textVisible:
                        screen.blit(menu_label, (width / 2 - menu_label.get_width() / 2,
                                                 height / 2 - menu_label.get_height() / 2))
                else:
                    self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.gameStarted and not self.gameOver:
                    position = pygame.mouse.get_pos()
                    rightClick = pygame.mouse.get_pressed()[2]
                    self.handleClick(position, rightClick)
                if event.type == pygame.KEYDOWN:
                    if not self.gameStarted:
                        self.gameStarted = True
                    elif self.gameOver:
                        self.resetGame()
                    if event.key == pygame.K_ESCAPE:
                        self.returnMenu()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()


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

game = Game(board, (width, height), menu_font)
game.run()
