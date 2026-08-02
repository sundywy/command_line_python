#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-11-13
Purpose: Python ls clone
"""

import argparse
from typing import List, NamedTuple


class Args(NamedTuple):
    """ Command-line arguments """
    paths: List[str]
    long: bool
    show_hidden: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Python ls clone',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('paths',
                        metavar='PATH',
                        nargs='*',
                        default=['.'],
                        help='Files and/or directories')

    parser.add_argument('-l',
                        '--long',
                        help='Long listing',
                        action='store_true')

    parser.add_argument('-a',
                        '--all',
                        help='Show all files',
                        action='store_true')

    args = parser.parse_args()

    return Args(paths=args.paths,
                long=args.long,
                show_hidden=args.all)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    _args = get_args()


# --------------------------------------------------
if __name__ == '__main__':
    main()
