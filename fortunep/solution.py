#!/usr/bin/env -S uv run --script
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-11-13
Purpose: Python fortune clone
"""

import argparse
from typing import List, NamedTuple, Optional


class Args(NamedTuple):
    """ Command-line arguments """
    sources: List[str]
    pattern: Optional[str]
    insensitive: bool
    seed: Optional[int]


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Python fortune clone',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('sources',
                        metavar='FILE',
                        nargs='+',
                        help='Input files or directories')

    parser.add_argument('-m',
                        '--pattern',
                        help='Pattern',
                        metavar='PATTERN',
                        type=str)

    parser.add_argument('-i',
                        '--insensitive',
                        help='Case-insensitive pattern matching',
                        action='store_true')

    parser.add_argument('-s',
                        '--seed',
                        help='Random seed',
                        metavar='SEED',
                        type=int)

    args = parser.parse_args()

    return Args(sources=args.sources,
                pattern=args.pattern,
                insensitive=args.insensitive,
                seed=args.seed)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    _args = get_args()


# --------------------------------------------------
if __name__ == '__main__':
    main()
