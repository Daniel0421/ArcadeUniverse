from tile import Tile
from random import random


class Board:
    def __init__(self, size, prob):
        self.size = size
        self.board = None
        self.prob = prob
        self.win = False
        self.lost = False
        self.numClicked = 0
        self.numNonBomb = 9
        self.initBoard()

    def initBoard(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                hasBomb = random() < self.prob
                if not hasBomb:
                    self.numNonBomb += 1
                tile = Tile(hasBomb)
                row.append(tile)
            self.board.append(row)
        self.setNeighbor()

    def setNeighbor(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                tile = self.getTile((row, col))
                neighbor = self.getListOfNeighbors((row, col))
                tile.setNeighbor(neighbor)

    def getListOfNeighbors(self, index):
        neighbor = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                outOfBoundary = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if same or outOfBoundary:
                    continue
                neighbor.append(self.getTile((row, col)))
        return neighbor

    def getSize(self):
        return self.size

    def getTile(self, index):
        return self.board[index[0]][index[1]]

    def handleClick(self, tile, flag):
        if tile.getClicked() or (not flag and tile.getFlagged()):
            return
        if flag:
            tile.toggleFlag()
            return
        tile.click()
        if tile.getHasBomb():
            self.lost = True
            return
        self.numClicked += 1
        if tile.getNeighbor() != 0:
            return
        for neighbor in tile.getNeighborList():
            if not neighbor.getHasBomb() and not neighbor.getClicked():
                self.handleClick(neighbor, False)

    def getLost(self):
        return self.lost

    def getWin(self):
        return self.numNonBomb == self.numClicked

