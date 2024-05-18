from game import Game
from board import Board

size = (9, 9)
prob = 0.5
board = Board(size, prob)
screenSize = (750, 750)
game = Game(board, screenSize)
game.run()