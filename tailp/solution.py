#!/usr/bin/env -S uv run --script
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2021-11-13
Purpose: Python tail clone
"""

import argparse
import re
import sys
from typing import List, NamedTuple, Optional


class Args(NamedTuple):
    """ Command-line arguments """
    files: List[str]
    lines: str
    bytes: Optional[str]
    quiet: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Python tail clone',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('files',
                        metavar='FILE',
                        nargs='+',
                        help='Input file(s)')

    parser.add_argument('-n',
                        '--lines',
                        help='Number of lines',
                        metavar='LINES',
                        type=str,
                        default='10')

    parser.add_argument('-c',
                        '--bytes',
                        help='Number of bytes',
                        metavar='BYTES',
                        type=str)

    parser.add_argument('-q',
                        '--quiet',
                        help='Suppress headers',
                        action='store_true')

    args = parser.parse_args()

    lines_given = any(
        a == '-n' or a.startswith('-n=') or a == '--lines'
        or a.startswith('--lines=') for a in sys.argv[1:])
    if args.bytes is not None and lines_given:
        parser.error("argument -c/--bytes: not allowed with argument "
                     "-n/--lines")

    num_re = re.compile(r'^([+-])?(\d+)$')

    if not num_re.search(args.lines):
        parser.error(f'illegal line count -- {args.lines}')

    if args.bytes is not None and not num_re.search(args.bytes):
        parser.error(f'illegal byte count -- {args.bytes}')

    return Args(files=args.files,
                lines=args.lines,
                bytes=args.bytes,
                quiet=args.quiet)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    _args = get_args()


# --------------------------------------------------
if __name__ == '__main__':
    main()
