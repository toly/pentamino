__author__ = 'toly'


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
