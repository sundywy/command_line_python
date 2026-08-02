#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-11-13
Purpose: Python cal clone
"""

import argparse
from typing import NamedTuple, Optional


class Args(NamedTuple):
    """ Command-line arguments """
    year: Optional[int]
    month: Optional[str]
    show_current_year: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Python cal clone',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('year',
                        help='Year (1-9999)',
                        metavar='YEAR',
                        nargs='?',
                        type=int)

    parser.add_argument('-m',
                        '--month',
                        help='Month name or number (1-12)',
                        metavar='MONTH')

    parser.add_argument('-y',
                        '--year',
                        help='Show the whole current year',
                        dest='show_current_year',
                        action='store_true')

    args = parser.parse_args()

    if args.year is not None and not 1 <= args.year <= 9999:
        parser.error(f"invalid value '{args.year}' for '[YEAR]': "
                     f'{args.year} is not in 1..=9999')

    if args.show_current_year and args.month is not None:
        parser.error("the argument '-m <MONTH>' cannot be used with '--year'")

    if args.show_current_year and args.year is not None:
        parser.error(
            "the argument '--year' cannot be used with '[YEAR]'")

    return Args(year=args.year,
                month=args.month,
                show_current_year=args.show_current_year)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    _args = get_args()


# --------------------------------------------------
if __name__ == '__main__':
    main()
