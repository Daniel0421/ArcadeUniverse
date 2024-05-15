from tile import Tile
from random import random
class Board:
    def __init__(self, size, prob):
        self.board = None
        self.prob = prob
        self.size = size
        self.initBoard()


    def initBoard(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                hasBomb = random() < self.prob
                tile = Tile(hasBomb)
                row.append(tile)
            self.board.append(row)
        self.setNeighbor()

    def setNeighbor(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                tile = self.getTile((row, col))
                neighbor = self.getNeighborList(tile)
                tile.setNeighbor(neighbor)

    def getNeighborList(self, index):
        neighbor = []
        for row in range(index[0]-1, index[0]+2) :
            for col in range(index[1]-1, index[1]+2):
                boundary = row < 0 or row >= self.size[0] or col <0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if same or boundary:
                    continue
                neighbor.append(self.getTile((row, col)))
        return neighbor






    def getSize(self):
        return self.size

    def getTile(self, index):
        return self.board[index[0]][index[1]]
