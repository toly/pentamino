__author__ = 'toly'

from base import BaseObject, Board, Figure


f = Figure([
    [1, 0, 0],
    [1, 1, 1],
])


board = Board(5, 8)
board.set_figure(f, 1, x=2)
board.set_figure(f, 2, x=0, y=4)
print board