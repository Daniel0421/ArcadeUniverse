class Board:
    def __init__(self, size):
        self.board = None
        self.size = size
        self.initBoard()

    def initBoard(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                tile = None
                row.append(tile)
            self.board.append(row)

    def getSize(self):
        return self.size
