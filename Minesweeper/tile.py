class Tile:
    def __init__(self, hasBomb):
        self.bomb = None
        self.neighbor = None
        self.hasBomb = hasBomb
        self.clicked = False
        self.flagged = False

    def getHasBomb(self):
        return self.hasBomb

    def getClicked(self):
        return self.clicked

    def getFlagged(self):
        return self.flagged

    def getNeighbor(self):
        return self.bomb

    def setNeighbor(self, neighbor):
        self.neighbor = neighbor
        self.boundary()

    def boundary(self):
        self.bomb = 0
        for tile in self.neighbor:
            if tile.getHasBomb():
                self.bomb += 1

    def getBoundary(self):
        return self.bomb

    def toggleFlag(self):
        self.flagged = not self.flagged

    def click(self):
        self.clicked = True

    def getNeighborList(self):
        return self.neighbor

