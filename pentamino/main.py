__author__ = 'toly'

from base import BaseObject, Board, Figure


f = Figure([
    [1, 0, 0],
    [1, 1, 0],
])

print f

print f.rotate_right()