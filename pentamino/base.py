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


def init_board(width, height):
    row = [0] * width
    return [list(row) for i in xrange(height)]


def set_figure(board, width, height, figure, color, x=0, y=0):
    new_board = map(list, board)

    if x < 0 or y < 0 or x + figure.width > width or y + figure.height > height:
        return

    for i, j in figure.points:
        if new_board[y+i][x+j] != 0:
            return
        new_board[y+i][x+j] = color

    return new_board


def get_free_cell(board, width, height):
    for i in xrange(height):
        for j in xrange(width):
            if board[i][j] == 0:
                return j, i


def print_board(board):
    result = ''
    for row in board:
        for cell in row:
            result += '{:3d}'.format(cell)
        result += '\n'
    print result


def pprint_board(matrix):
    """
        pretty print board

        board like:
        [
            [1, 2, 2],
            [2, 2, 2],
            [2, 3, 3],
            [2, 4, 3],
        ]

        will be printed as:
        +---+---+---+
        |   |       |
        +---+       +
        |           |
        +   +---+---+
        |   |       |
        +   +---+   +
        |   |   |   |
        +---+---+---+
    """
    WIDTH_FACTOR = 3

    height, width = len(matrix), len(matrix[0])
    new_height, new_width = map(lambda x: 2 * x + 1, (height, width))

    new_matrix = init_board(new_width, new_height)

    for y in xrange(height):
        for x in xrange(width):
            new_x, new_y = map(lambda n: 2 * n + 1, (x, y))
            new_matrix[new_y][new_x] = matrix[y][x]

    def is_odd(x):
        return bool(x % 2)

    for y in xrange(new_height):
        for x in xrange(new_width):

            # corners
            if (x, y) in ((0, 0), (0, new_height - 1), (new_width - 1, 0), (new_width - 1, new_height - 1)):
                new_matrix[y][x] = '+'
                continue

            # top-bottom border lines
            if is_odd(x) and y in (0, new_height - 1):
                new_matrix[y][x] = '-' * WIDTH_FACTOR
                continue

            # right-left border lines
            if is_odd(y) and x in (0, new_width - 1):
                new_matrix[y][x] = '|'
                continue

            # verical line or space between cells
            if not is_odd(x) and is_odd(y):
                if new_matrix[y][x-1] != new_matrix[y][x+1]:
                    new_matrix[y][x] = '|'
                else:
                    new_matrix[y][x] = ' '
                continue

            # horizontal line or space between cells
            if not is_odd(y) and is_odd(x):
                if new_matrix[y+1][x] != new_matrix[y-1][x]:
                    new_matrix[y][x] = '-' * WIDTH_FACTOR
                else:
                    new_matrix[y][x] = ' ' * WIDTH_FACTOR
                continue

            # inner and border corners or spaces
            if not is_odd(x) and not is_odd(y):
                new_matrix[y][x] = '+'
                if 0 < x < new_width - 1 and 0 < y < new_height - 1:
                    cells = (new_matrix[y-1][x-1], new_matrix[y+1][x-1], new_matrix[y-1][x+1], new_matrix[y+1][x+1], )
                    if len(set(cells)) == 1:
                        new_matrix[y][x] = ' '

    for y in xrange(new_height):
        for x in xrange(new_width):
            if type(new_matrix[y][x]) is int:
                new_matrix[y][x] = ' ' * WIDTH_FACTOR

    for row in new_matrix:
        print ''.join(map(str, row))


def reflect_board(board):
    return board[::-1]


def rotate_right(board):
    height, width = len(board), len(board[0])
    new_board = []

    for j in xrange(width):
        new_row = []
        for i in xrange(height - 1, -1, -1):
            new_row.append(board[i][j])
        new_board.append(new_row)

    return new_board


def generate_shadows(board):

    original_board = map(list, board)
    yield original_board

    reflected_board = reflect_board(original_board)
    yield reflected_board

    for i in xrange(3):
        original_board = rotate_right(original_board)
        reflected_board = rotate_right(reflected_board)
        yield original_board
        yield reflected_board


def board_hash(board):
    rows = []
    for row in board:
        rows.append(','.join(map(str, row)))
    return '+'.join(rows)


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

        points = []
        for i in xrange(self.height):
            for j in xrange(self.width):
                if self.data[i][j]:
                    points.append((i, j))

        self.points = tuple(points)

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
