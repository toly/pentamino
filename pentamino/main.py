__author__ = 'toly'

from base import BaseObject, Board, Figure


f = Figure([
    [1, 0, 0],
    [1, 1, 1],
])


for figure in Figure.generate_shadows(f.data):
    print '-' * 10
    print figure