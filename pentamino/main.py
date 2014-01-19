#!/usr/bin/env python
__author__ = 'toly'

import time
import copy

from base import Board, Figure, BadPlacingError
from settings import WIDTH, HEIGHT, FIGURES_RAW


def make_decisions(board, figures_dict, order):

    if not figures_dict:
        yield board
        return

    x, y = board.get_free_cell()

    for figure_color, figures_list in figures_dict.items():
        for figure in figures_list:

            current_board = copy.deepcopy(board)
            current_figures_dict = copy.deepcopy(figures_dict)
            current_order = copy.deepcopy(order)

            try:
                current_board.set_figure(figure, figure_color, x=x-figure.shift, y=y)
            except BadPlacingError:
                pass
            else:

                if current_board.have_isolated_cells():
                    continue

                del current_figures_dict[figure_color]
                current_order.append(figure_color)
                for decision_board in make_decisions(current_board, current_figures_dict, current_order):
                    if decision_board:
                        yield decision_board


if __name__ == '__main__':
    board = Board(WIDTH, HEIGHT)
    figures_dict = Figure.generate_figures_dict(FIGURES_RAW)

    time_start = time.time()

    n = 0
    for decision in make_decisions(board, figures_dict, []):
        n += 1
        print 'decision #%d' % n

        print decision

        if n >= 10:
            break

    print time.time() - time_start
