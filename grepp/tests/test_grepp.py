""" Tests for grepp """

import os
import platform
import random
import re
import string
from pathlib import Path
from subprocess import getstatusoutput, run
from typing import List

PRG: str = './grepp.py'
RUN: str = f'python {PRG}' if platform.system() == 'Windows' else PRG
BUSTLE: str = 'tests/inputs/bustle.txt'
EMPTY: str = 'tests/inputs/empty.txt'
FOX: str = 'tests/inputs/fox.txt'
NOBODY: str = 'tests/inputs/nobody.txt'
INPUTS_DIR: str = 'tests/inputs'


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
def test_dies_no_args() -> None:
    """ Dies with no arguments """

    rv, out = getstatusoutput(PRG)
    assert rv != 0
    assert out.lower().startswith('usage')


# --------------------------------------------------
def test_dies_bad_pattern() -> None:
    """ Dies on bad regex pattern """

    rv, out = getstatusoutput(f'{RUN} "*foo" {FOX}')
    assert rv != 0
    assert 'Invalid pattern "*foo"' in out


# --------------------------------------------------
def test_warns_bad_file() -> None:
    """ Warns on bad file """

    bad = gen_bad_file()
    res = run([PRG, 'foo', bad], capture_output=True, text=True)
    assert re.search(f'{bad}: .*No such file or directory', res.stderr)


# --------------------------------------------------
def run_test(args: List[str], expected_file: str) -> None:
    """ Test with input """

    windows_file = f'{expected_file}.windows'
    if platform.system() == 'Windows' and os.path.isfile(windows_file):
        expected_file = windows_file

    assert os.path.isfile(expected_file)
    expected = Path(expected_file).read_text()

    res = run([PRG] + args, capture_output=True, text=True)
    assert res.returncode == 0
    assert res.stdout == expected


# --------------------------------------------------
def test_empty_file() -> None:
    """ Empty file """

    run_test(['foo', EMPTY], 'tests/expected/empty.foo')


# --------------------------------------------------
def test_empty_regex() -> None:
    """ Empty regex """

    run_test(['', FOX], 'tests/expected/empty_regex.fox.txt')


# --------------------------------------------------
def test_bustle_capitalized() -> None:
    """ Bustle capitalized """

    run_test(['The', BUSTLE], 'tests/expected/bustle.txt.the.capitalized')


# --------------------------------------------------
def test_bustle_lowercase() -> None:
    """ Bustle lowercase """

    run_test(['the', BUSTLE], 'tests/expected/bustle.txt.the.lowercase')


# --------------------------------------------------
def test_bustle_insensitive() -> None:
    """ Bustle insensitive """

    run_test(['--insensitive', 'the', BUSTLE],
             'tests/expected/bustle.txt.the.lowercase.insensitive')


# --------------------------------------------------
def test_nobody() -> None:
    """ Nobody """

    run_test(['nobody', NOBODY], 'tests/expected/nobody.txt')


# --------------------------------------------------
def test_nobody_insensitive() -> None:
    """ Nobody insensitive """

    run_test(['-i', 'nobody', NOBODY],
             'tests/expected/nobody.txt.insensitive')


# --------------------------------------------------
def test_multiple_files() -> None:
    """ Multiple files """

    run_test(['The', BUSTLE, EMPTY, FOX, NOBODY],
             'tests/expected/all.the.capitalized')


# --------------------------------------------------
def test_multiple_files_insensitive() -> None:
    """ Multiple files insensitive """

    run_test(['-i', 'the', BUSTLE, EMPTY, FOX, NOBODY],
             'tests/expected/all.the.lowercase.insensitive')


# --------------------------------------------------
def test_recursive() -> None:
    """ Recursive """

    run_test(['--recursive', 'dog', INPUTS_DIR],
             'tests/expected/dog.recursive')


# --------------------------------------------------
def test_recursive_insensitive() -> None:
    """ Recursive insensitive """

    run_test(['-ri', 'then', INPUTS_DIR],
             'tests/expected/the.recursive.insensitive')


# --------------------------------------------------
def test_sensitive_count_capital() -> None:
    """ Sensitive count capital """

    run_test(['--count', 'The', BUSTLE],
             'tests/expected/bustle.txt.the.capitalized.count')


# --------------------------------------------------
def test_sensitive_count_lower() -> None:
    """ Sensitive count lower """

    run_test(['--count', 'the', BUSTLE],
             'tests/expected/bustle.txt.the.lowercase.count')


# --------------------------------------------------
def test_insensitive_count() -> None:
    """ Insensitive count """

    run_test(['-ci', 'the', BUSTLE],
             'tests/expected/bustle.txt.the.lowercase.insensitive.count')


# --------------------------------------------------
def test_nobody_count() -> None:
    """ Nobody count """

    run_test(['-c', 'nobody', NOBODY], 'tests/expected/nobody.txt.count')


# --------------------------------------------------
def test_nobody_count_insensitive() -> None:
    """ Nobody count insensitive """

    run_test(['-ci', 'nobody', NOBODY],
             'tests/expected/nobody.txt.insensitive.count')


# --------------------------------------------------
def test_sensitive_count_multiple() -> None:
    """ Sensitive count multiple """

    run_test(['-c', 'The', BUSTLE, EMPTY, FOX, NOBODY],
             'tests/expected/all.the.capitalized.count')


# --------------------------------------------------
def test_insensitive_count_multiple() -> None:
    """ Insensitive count multiple """

    run_test(['-ic', 'the', BUSTLE, EMPTY, FOX, NOBODY],
             'tests/expected/all.the.lowercase.insensitive.count')


# --------------------------------------------------
def test_warns_dir_not_recursive() -> None:
    """ Warns when directory given without -r """

    stdout = ('tests/inputs/fox.txt:'
              'The quick brown fox jumps over the lazy dog.')
    res = run([PRG, 'fox', INPUTS_DIR, FOX], capture_output=True, text=True)
    assert 'tests/inputs is a directory' in res.stderr
    assert stdout in res.stdout


# --------------------------------------------------
def test_stdin() -> None:
    """ Stdin """

    expected = Path('tests/expected/bustle.txt.the.capitalized').read_text()
    input_text = Path(BUSTLE).read_text()
    res = run([PRG, 'The'], input=input_text, capture_output=True, text=True)
    assert res.returncode == 0
    assert res.stdout == expected


# --------------------------------------------------
def test_stdin_insensitive_count() -> None:
    """ Stdin insensitive count """

    files = [BUSTLE, EMPTY, FOX, NOBODY]
    input_text = ''.join(Path(f).read_text() for f in files)
    expected = Path(
        'tests/expected/the.recursive.insensitive.count.stdin').read_text()
    res = run([PRG, '-ci', 'the', '-'],
              input=input_text,
              capture_output=True,
              text=True)
    assert res.returncode == 0
    assert res.stdout == expected
