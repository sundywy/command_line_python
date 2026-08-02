#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-11-13
Purpose: Python grep clone
"""

import argparse
from typing import List, NamedTuple


class Args(NamedTuple):
    """ Command-line arguments """
    pattern: str
    files: List[str]
    insensitive: bool
    recursive: bool
    count: bool
    invert: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Python grep clone',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('pattern', metavar='PATTERN', help='Search pattern')

    parser.add_argument('files',
                        metavar='FILE',
                        nargs='*',
                        default=['-'],
                        help='Input file(s)')

    parser.add_argument('-i',
                        '--insensitive',
                        help='Case-insensitive search',
                        action='store_true')

    parser.add_argument('-r',
                        '--recursive',
                        help='Recursive search',
                        action='store_true')

    parser.add_argument('-c',
                        '--count',
                        help='Count occurrences',
                        action='store_true')

    parser.add_argument('-v',
                        '--invert-match',
                        help='Invert match',
                        action='store_true')

    args = parser.parse_args()

    return Args(pattern=args.pattern,
                files=args.files,
                insensitive=args.insensitive,
                recursive=args.recursive,
                count=args.count,
                invert=args.invert_match)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    _args = get_args()


# --------------------------------------------------
if __name__ == '__main__':
    main()
