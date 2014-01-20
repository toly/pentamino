#!/usr/bin/env python
__author__ = 'toly'

import time

from base import Board, Figure, BadPlacingError
from settings import WIDTH, HEIGHT, FIGURES_RAW


def make_decisions(board, figures_dict, order):

    if not figures_dict:
        yield board
        return

    x, y = board.get_free_cell()

    for figure_color, figures_list in figures_dict.items():
        for figure in figures_list:

            current_board = Board(board.width, board.height, board.data)
            current_figures_dict = dict(figures_dict)
            current_order = list(order)

            try:
                current_board.set_figure(figure, figure_color, x=x-figure.shift, y=y)
            except BadPlacingError:
                continue

            del current_figures_dict[figure_color]
            current_order.append(figure_color)
            for decision_board in make_decisions(current_board, current_figures_dict, current_order):
                if decision_board:
                    yield decision_board


if __name__ == '__main__':
    board = Board(WIDTH, HEIGHT)
    figures_dict = Figure.generate_figures_dict(FIGURES_RAW)

    board.set_figure(figures_dict[13][0], 13, 3, 3)
    del figures_dict[13]

    time_start0 = time.time()
    time_start = time_start0

    n = 0
    for decision in make_decisions(board, figures_dict, []):
        time_solve = time.time() - time_start
        n += 1
        print 'decision #%d' % n
        print 'solved by %f seconds' % time_solve

        print decision

        # if n >= 10:
        #     break

        time_start = time.time()

    print 'total time:', time.time() - time_start0