""" Tests for lsp """

import os
import platform
import random
import string
from subprocess import getstatusoutput, run
from typing import List, Tuple

PRG: str = './lsp.py'
RUN: str = f'python {PRG}' if platform.system() == 'Windows' else PRG
HIDDEN: str = 'tests/inputs/.hidden'
EMPTY: str = 'tests/inputs/empty.txt'
BUSTLE: str = 'tests/inputs/bustle.txt'
FOX: str = 'tests/inputs/fox.txt'


# --------------------------------------------------
def test_exists() -> None:
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage() -> None:
    """ Prints usage """

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{RUN} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def random_string() -> str:
    """ Generate a random string """

    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))


# --------------------------------------------------
def gen_bad_file() -> str:
    """ Generate a bad filename """

    while True:
        filename = random_string()
        if not os.path.isfile(filename):
            return filename


# --------------------------------------------------
def test_bad_file() -> None:
    """ Warns on bad file """

    bad = gen_bad_file()
    res = run([PRG, bad], capture_output=True, text=True)
    assert res.returncode == 0
    assert f'{bad}: No such file or directory' in res.stderr


# --------------------------------------------------
def test_no_args() -> None:
    """ Uses current directory by default """

    res = run([PRG], capture_output=True, text=True)
    assert res.returncode == 0
    assert 'lsp.py' in res.stdout


# --------------------------------------------------
def run_short(arg: str) -> None:
    """ Short listing of a file """

    res = run([PRG, arg], capture_output=True, text=True)
    assert res.returncode == 0
    assert res.stdout == f'{arg}\n'


# --------------------------------------------------
def run_long(filename: str, permissions: str, size: str) -> None:
    """ Long listing of a file """

    res = run([PRG, '--long', filename], capture_output=True, text=True)
    assert res.returncode == 0
    parts = res.stdout.split()
    assert parts[0] == permissions
    assert parts[4] == size
    assert parts[-1] == filename


# --------------------------------------------------
def test_empty() -> None:
    """ Empty file """

    run_short(EMPTY)


# --------------------------------------------------
def test_empty_long() -> None:
    """ Empty file long """

    run_long(EMPTY, '-rw-r--r--', '0')


# --------------------------------------------------
def test_bustle() -> None:
    """ Bustle file """

    run_short(BUSTLE)


# --------------------------------------------------
def test_bustle_long() -> None:
    """ Bustle file long """

    run_long(BUSTLE, '-rw-r--r--', '193')


# --------------------------------------------------
def test_fox() -> None:
    """ Fox file """

    run_short(FOX)


# --------------------------------------------------
def test_fox_long() -> None:
    """ Fox file long """

    run_long(FOX, '-rw-------', '45')


# --------------------------------------------------
def test_hidden() -> None:
    """ Hidden file """

    run_short(HIDDEN)


# --------------------------------------------------
def test_hidden_long() -> None:
    """ Hidden file long """

    run_long(HIDDEN, '-rw-r--r--', '0')


# --------------------------------------------------
def dir_short(args: List[str], expected: List[str]) -> None:
    """ Directory short listing """

    res = run([PRG] + args, capture_output=True, text=True)
    assert res.returncode == 0
    lines = [line for line in res.stdout.split('\n') if line]
    assert len(lines) == len(expected)
    for filename in expected:
        assert filename in lines


# --------------------------------------------------
def test_dir1() -> None:
    """ Directory listing """

    dir_short(
        ['tests/inputs'],
        [
            'tests/inputs/empty.txt',
            'tests/inputs/bustle.txt',
            'tests/inputs/fox.txt',
            'tests/inputs/dir',
        ],
    )


# --------------------------------------------------
def test_dir1_all() -> None:
    """ Directory listing with --all """

    dir_short(
        ['tests/inputs', '--all'],
        [
            'tests/inputs/empty.txt',
            'tests/inputs/bustle.txt',
            'tests/inputs/fox.txt',
            'tests/inputs/.hidden',
            'tests/inputs/dir',
        ],
    )


# --------------------------------------------------
def test_dir2() -> None:
    """ Subdirectory listing """

    dir_short(['tests/inputs/dir'], ['tests/inputs/dir/spiders.txt'])


# --------------------------------------------------
def test_dir2_all() -> None:
    """ Subdirectory listing with -a """

    dir_short(
        ['-a', 'tests/inputs/dir'],
        ['tests/inputs/dir/spiders.txt', 'tests/inputs/dir/.gitkeep'],
    )


# --------------------------------------------------
def dir_long(args: List[str],
             expected: List[Tuple[str, str, str]]) -> None:
    """ Directory long listing """

    res = run([PRG] + args, capture_output=True, text=True)
    assert res.returncode == 0
    lines = [line for line in res.stdout.split('\n') if line]
    assert len(lines) == len(expected)

    check = []
    for line in lines:
        parts = line.split()
        path = parts[-1]
        permissions = parts[0]
        size = '' if permissions.startswith('d') else parts[4]
        check.append((path, permissions, size))

    for entry in expected:
        assert entry in check


# --------------------------------------------------
def test_dir1_long() -> None:
    """ Directory long listing """

    dir_long(
        ['-l', 'tests/inputs'],
        [
            ('tests/inputs/empty.txt', '-rw-r--r--', '0'),
            ('tests/inputs/bustle.txt', '-rw-r--r--', '193'),
            ('tests/inputs/fox.txt', '-rw-------', '45'),
            ('tests/inputs/dir', 'drwxr-xr-x', ''),
        ],
    )


# --------------------------------------------------
def test_dir1_long_all() -> None:
    """ Directory long listing with -a """

    dir_long(
        ['-la', 'tests/inputs'],
        [
            ('tests/inputs/empty.txt', '-rw-r--r--', '0'),
            ('tests/inputs/bustle.txt', '-rw-r--r--', '193'),
            ('tests/inputs/fox.txt', '-rw-------', '45'),
            ('tests/inputs/dir', 'drwxr-xr-x', ''),
            ('tests/inputs/.hidden', '-rw-r--r--', '0'),
        ],
    )


# --------------------------------------------------
def test_dir2_long() -> None:
    """ Subdirectory long listing """

    dir_long(
        ['--long', 'tests/inputs/dir'],
        [('tests/inputs/dir/spiders.txt', '-rw-r--r--', '45')],
    )


# --------------------------------------------------
def test_dir2_long_all() -> None:
    """ Subdirectory long listing with --all """

    dir_long(
        ['tests/inputs/dir', '--long', '--all'],
        [
            ('tests/inputs/dir/spiders.txt', '-rw-r--r--', '45'),
            ('tests/inputs/dir/.gitkeep', '-rw-r--r--', '0'),
        ],
    )
