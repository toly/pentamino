#!/usr/bin/env python
__author__ = 'toly'

import time
from argparse import ArgumentParser

from base import Figure, init_board, set_figure, get_free_cell, print_board, pprint_board
from settings import WIDTH, HEIGHT, FIGURES_RAW


def main():
    """entry point"""
    argparser = create_argparser()
    args = argparser.parse_args()

    board = init_board(WIDTH, HEIGHT)
    figures_dict = Figure.generate_figures_dict(FIGURES_RAW)

    if args.center_square:
        board = set_figure(board, WIDTH, HEIGHT, figures_dict[13][0], 13, 3, 3)
        del figures_dict[13]

    time_start0 = time.time()
    time_start = time_start0

    n = 0
    for decision in make_decisions(board, WIDTH, HEIGHT, figures_dict):
        time_solve = time.time() - time_start
        n += 1
        print 'decision #%d' % n
        print 'solved by %f seconds' % time_solve

        pprint_board(decision)

        if args.number_decisions and n >= args.number_decisions:
            break

        time_start = time.time()

    print 'total time:', time.time() - time_start0


def create_argparser():
    parser = ArgumentParser()
    parser.add_argument('-n', '--number-decisions', type=int, help="need decisions count")
    parser.add_argument('-c', '--center-square', action="store_true", help="show decisions where "
                                                                           "square figure placed in center")

    return parser


def make_decisions(board, width, height, figures_dict):

    if not figures_dict:
        yield board
        return

    x, y = get_free_cell(board, width, height)

    for figure_color, figures_list in figures_dict.items():
        for figure in figures_list:

            current_board = set_figure(board, width, height, figure, figure_color, x=x-figure.shift, y=y)

            if current_board is None:
                continue

            current_figures_dict = dict(figures_dict)
            del current_figures_dict[figure_color]

            for decision_board in make_decisions(current_board, width, height, current_figures_dict):
                if not decision_board is None:
                    yield decision_board


if __name__ == '__main__':
    main()