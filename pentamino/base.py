__author__ = 'toly'

import itertools


class BaseObject(object):
    """
        Base object with show method
    """

    data = None

    def __str__(self):
        result = ''
        for row in self.data:
            for cell in row:
                result += '{:3d}'.format(cell)
            result += '\n'
        return result


class Board(BaseObject):
    width = None
    height = None

    def __init__(self, width, heigh):
        self.width, self.height = width, heigh
        self.data = []

        row = [0] * width
        for i in xrange(heigh):
            self.data.append(list(row))


class Figure(BaseObject):
    data = None
    width = None
    height = None

    shift = None
    hash_key = None

    def __init__(self, data):

        self.data = data
        self.check_size()
        self.check_single_color()

        self.shift = self.data[0].index(1)

    def check_size(self):
        width = None
        for i in xrange(len(self.data)):
            next_width = len(self.data[i])
            if next_width == 0:
                raise Exception('Empty row')
            if not width is None and width != next_width:
                raise Exception('Different lengths of rows')
            width = next_width

    def check_single_color(self):
        all_colors = set(itertools.chain(*self.data))
        not_null_colors = list(all_colors - {0})
        if len(not_null_colors) == 0:
            raise Exception('Empty figure')
        if len(not_null_colors) > 1:
            raise Exception('Too many colors')
        if not_null_colors[0] != 1:
            raise Exception('Need only one color: 1')