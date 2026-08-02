""" Tests for fortunep """

import os
import platform
import random
import re
import string
from pathlib import Path
from subprocess import getstatusoutput, run
from typing import List

PRG: str = './fortunep.py'
RUN: str = f'python {PRG}' if platform.system() == 'Windows' else PRG
FORTUNE_DIR: str = './tests/inputs'
EMPTY_DIR: str = './tests/inputs/empty'
JOKES: str = './tests/inputs/jokes'
LITERATURE: str = './tests/inputs/literature'
QUOTES: str = './tests/inputs/quotes'


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
def test_dies_not_enough_args() -> None:
    """ Dies with no arguments """

    rv, out = getstatusoutput(PRG)
    assert rv != 0
    assert out.lower().startswith('usage')


# --------------------------------------------------
def test_dies_bad_file() -> None:
    """ Dies on bad file """

    bad = gen_bad_file()
    rv, out = getstatusoutput(f'{RUN} {LITERATURE} {bad}')
    assert rv != 0
    assert re.search(f'{bad}: .*No such file or directory', out)


# --------------------------------------------------
def test_dies_bad_pattern() -> None:
    """ Dies on bad pattern """

    rv, out = getstatusoutput(f'{RUN} --pattern "*" {LITERATURE}')
    assert rv != 0
    assert 'Invalid --pattern "*"' in out


# --------------------------------------------------
def test_dies_bad_seed() -> None:
    """ Dies on bad seed """

    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} {LITERATURE} --seed {bad}')
    assert rv != 0
    assert out.lower().startswith('usage')


# --------------------------------------------------
def run_test(args: List[str], expected: str) -> None:
    """ Test stdout against expected string """

    res = run([PRG] + args, capture_output=True, text=True)
    assert res.returncode == 0
    assert res.stdout == expected


# --------------------------------------------------
def run_outfiles(args: List[str], out_file: str, err_file: str) -> None:
    """ Test stdout/stderr against expected files """

    expected_out = Path(out_file).read_text()
    expected_err = Path(err_file).read_text()

    res = run([PRG] + args, capture_output=True, text=True)
    assert res.returncode == 0
    assert res.stdout == expected_out
    assert res.stderr == expected_err


# --------------------------------------------------
def test_no_fortunes_found() -> None:
    """ No fortunes found """

    run_test([EMPTY_DIR], 'No fortunes found\n')


# --------------------------------------------------
def test_quotes_seed_1() -> None:
    """ Quotes with seed 1 """

    # Expected value from random.seed(1) / random.choice over quotes
    run_test(
        [QUOTES, '-s', '1'],
        'I can live for two months on a good compliment.\n-- Mark Twain\n',
    )


# --------------------------------------------------
def test_jokes_seed_1() -> None:
    """ Jokes with seed 1 """

    run_test(
        [JOKES, '-s', '1'],
        "Q: Why did the gardener quit his job?\n"
        "A: His celery wasn't high enough.\n",
    )


# --------------------------------------------------
def test_dir_seed_10() -> None:
    """ Directory with seed 10 """

    run_test(
        [FORTUNE_DIR, '-s', '10'],
        'You can observe a lot just by watching.\n-- Yogi Berra\n',
    )


# --------------------------------------------------
def test_yogi_berra_cap() -> None:
    """ Yogi Berra capitalized """

    run_outfiles(['--pattern', 'Yogi Berra', FORTUNE_DIR],
                 'tests/expected/berra_cap.out',
                 'tests/expected/berra_cap.err')


# --------------------------------------------------
def test_mark_twain_cap() -> None:
    """ Mark Twain capitalized """

    run_outfiles(['-m', 'Mark Twain', FORTUNE_DIR],
                 'tests/expected/twain_cap.out',
                 'tests/expected/twain_cap.err')


# --------------------------------------------------
def test_yogi_berra_lower() -> None:
    """ Yogi Berra lowercase """

    run_outfiles(['--pattern', 'yogi berra', FORTUNE_DIR],
                 'tests/expected/berra_lower.out',
                 'tests/expected/berra_lower.err')


# --------------------------------------------------
def test_mark_twain_lower() -> None:
    """ Mark Twain lowercase """

    run_outfiles(['-m', 'will twain', FORTUNE_DIR],
                 'tests/expected/twain_lower.out',
                 'tests/expected/twain_lower.err')


# --------------------------------------------------
def test_yogi_berra_lower_i() -> None:
    """ Yogi Berra lowercase insensitive """

    run_outfiles(
        ['--insensitive', '--pattern', 'yogi berra', FORTUNE_DIR],
        'tests/expected/berra_lower_i.out',
        'tests/expected/berra_lower_i.err',
    )


# --------------------------------------------------
def test_mark_twain_lower_i() -> None:
    """ Mark Twain lowercase insensitive """

    run_outfiles(['-i', '-m', 'mark twain', FORTUNE_DIR],
                 'tests/expected/twain_lower_i.out',
                 'tests/expected/twain_lower_i.err')
