__author__ = 'toly'


class BaseObject(object):
    """
        Base object with show method
    """

    data = None

    def __str__(self):
        if self.data is None:
            print '<BaseObject: empty>'
            return ''

        for row in self.data:
            for cell in row:
                print '{:3d}'.format(cell),
            print
        print

        return ''