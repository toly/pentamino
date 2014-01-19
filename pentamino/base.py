__author__ = 'toly'

import itertools


class BadPlacingError(Exception):
    pass


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

    def __init__(self, width, heigh, data=None):
        self.width, self.height = width, heigh
        self.data = []

        if data is None:
            row = [0] * width
            for i in xrange(heigh):
                self.data.append(list(row))
        else:
            for row in data:
                self.data.append(list(row))

    def set_figure(self, figure, color, x=0, y=0):

        if color == 0:
            raise Exception('Color must be more than zero')

        if x < 0 or y < 0 or x + figure.width > self.width or y + figure.height > self.height:
            raise BadPlacingError

        for i in xrange(figure.height):
            for j in xrange(figure.width):

                if figure.data[i][j] == 0:
                    continue

                if self.data[y+i][x+j] != 0:
                    raise BadPlacingError

                self.data[y+i][x+j] = color

    def get_free_cell(self):
        for i in xrange(self.height):
            for j in xrange(self.width):
                if self.data[i][j] == 0:
                    return j, i

    def get_cell(self, x, y):
        return self.data[y][x]

    def nearest_coords_cells(self, x, y):
        for i in xrange(-1, 2):
            for j in xrange(-1, 2):
                if x + i < 0 or y + j < 0:
                    continue
                if i == 0 and j == 0:
                    continue
                if x + i > self.width - 1 or y + j > self.height - 1:
                    continue

                yield x + i, y + j

    def cell_isolated(self, x, y):
        for i, j in self.nearest_coords_cells(x, y):
            if not self.get_cell(i, j):
                return False
        return True

    def have_isolated_cells(self):
        for i in xrange(self.width):
            for j in xrange(self.height):
                if self.get_cell(i, j) != 0:
                    continue
                if self.cell_isolated(i, j):
                    return True
        return False


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

        self.height = len(self.data)
        self.width = len(self.data[0])
        self.shift = self.data[0].index(1)
        self.hash_key = self.get_key_hash()

    def check_size(self):
        width = None
        for i in xrange(len(self.data)):
            next_width = len(self.data[i])
            if next_width == 0:
                raise Exception('Empty row')
            if not width is None and width != next_width:

                print self.data

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

    def rotate_right(self):

        new_data = []
        for j in xrange(self.width):
            new_row = []
            for i in xrange(self.height - 1, -1, -1):
                new_row.append(self.data[i][j])
            new_data.append(new_row)

        return Figure(new_data)

    def reflection(self):
        new_data = self.data[::-1]
        return Figure(new_data)

    def get_key_hash(self):
        rows = []
        for row in self.data:
            rows.append(','.join(map(str, row)))
        return '+'.join(rows)

    @classmethod
    def generate_shadows(cls, init_figure_data):
        init_figure = cls(init_figure_data)
        result, hashes = [init_figure], [init_figure.hash_key]

        reflect_figure = init_figure.reflection()
        if reflect_figure.hash_key not in hashes:
            result.append(reflect_figure)
            hashes.append(reflect_figure.hash_key)

        for i in xrange(3):
            init_figure = init_figure.rotate_right()
            reflect_figure = reflect_figure.rotate_right()

            for figure in [init_figure, reflect_figure]:
                if figure.hash_key not in hashes:
                    result.append(figure)
                    hashes.append(figure.hash_key)

        return result

    @classmethod
    def generate_figures_dict(cls, figures_raw_list):
        result = {}
        for index, figure_raw in enumerate(figures_raw_list):
            result[index + 1] = Figure.generate_shadows(figure_raw)
        return result
