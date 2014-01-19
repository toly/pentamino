__author__ = 'toly'

from base import BaseObject, Board


a = BaseObject()
a.data = [
    [1, 2, 3],
    [1, 3, 3]
]

print a


b = Board(3, 4)
b.data[0][0] = 12
print b