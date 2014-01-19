__author__ = 'toly'

from base import BaseObject, Board, Figure


f = Figure([
    [1, 0, 0],
    [1, 1, 1],
])


board = Board(5, 8)
board.set_figure(f, 1)
print board

print board.get_free_cell()