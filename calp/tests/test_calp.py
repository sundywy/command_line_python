""" Tests for calp """

import os
import platform
from pathlib import Path
from subprocess import getstatusoutput, run
from typing import List

PRG: str = './calp.py'
RUN: str = f'python {PRG}' if platform.system() == 'Windows' else PRG


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
def test_dies_year_0() -> None:
    """ Dies on year 0 """

    rv, out = getstatusoutput(f'{RUN} 0')
    assert rv != 0
    assert '0 is not in 1..=9999' in out or 'invalid' in out.lower()


# --------------------------------------------------
def test_dies_year_10000() -> None:
    """ Dies on year 10000 """

    rv, out = getstatusoutput(f'{RUN} 10000')
    assert rv != 0
    assert '10000 is not in 1..=9999' in out or 'invalid' in out.lower()


# --------------------------------------------------
def test_dies_invalid_year() -> None:
    """ Dies on invalid year """

    rv, out = getstatusoutput(f'{RUN} foo')
    assert rv != 0
    assert out.lower().startswith('usage')


# --------------------------------------------------
def test_dies_month_0() -> None:
    """ Dies on month 0 """

    res = run([PRG, '-m', '0'], capture_output=True, text=True)
    assert res.returncode != 0
    assert res.stdout == ''
    assert res.stderr.strip() == 'month "0" not in the range 1 through 12'


# --------------------------------------------------
def test_dies_month_13() -> None:
    """ Dies on month 13 """

    res = run([PRG, '-m', '13'], capture_output=True, text=True)
    assert res.returncode != 0
    assert res.stderr.strip() == 'month "13" not in the range 1 through 12'


# --------------------------------------------------
def test_dies_invalid_month() -> None:
    """ Dies on invalid month """

    res = run([PRG, '-m', 'foo'], capture_output=True, text=True)
    assert res.returncode != 0
    assert res.stderr.strip() == 'Invalid month "foo"'


# --------------------------------------------------
def test_dies_y_and_month() -> None:
    """ Dies when -y and -m used together """

    rv, out = getstatusoutput(f'{RUN} -m 1 -y')
    assert rv != 0
    assert out.lower().startswith('usage')


# --------------------------------------------------
def test_dies_y_and_year() -> None:
    """ Dies when -y and year used together """

    rv, out = getstatusoutput(f'{RUN} -y 2000')
    assert rv != 0
    assert out.lower().startswith('usage')


# --------------------------------------------------
def test_month_num() -> None:
    """ Month numbers """

    expected = [
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    for num, month in expected:
        res = run([PRG, '-m', num], capture_output=True, text=True)
        assert res.returncode == 0
        assert month in res.stdout


# --------------------------------------------------
def test_partial_month() -> None:
    """ Partial month names """

    expected = [
        ('ja', 'January'),
        ('f', 'February'),
        ('mar', 'March'),
        ('ap', 'April'),
        ('may', 'May'),
        ('jun', 'June'),
        ('jul', 'July'),
        ('au', 'August'),
        ('s', 'September'),
        ('n', 'November'),
        ('d', 'December'),
    ]

    for arg, month in expected:
        res = run([PRG, '-m', arg], capture_output=True, text=True)
        assert res.returncode == 0
        assert month in res.stdout


# --------------------------------------------------
def run_test(args: List[str], expected_file: str) -> None:
    """ Test with input """

    assert os.path.isfile(expected_file)
    expected = Path(expected_file).read_text()

    res = run([PRG] + args, capture_output=True, text=True)
    assert res.returncode == 0
    assert res.stdout == expected


# --------------------------------------------------
def test_default_one_month() -> None:
    """ Default shows one month """

    res = run([PRG], capture_output=True, text=True)
    assert res.returncode == 0
    lines = res.stdout.split('\n')
    assert len(lines) == 9
    assert len(lines[0]) == 22


# --------------------------------------------------
def test_2_2020_leap_year() -> None:
    """ February 2020 leap year """

    run_test(['-m', '2', '2020'], 'tests/expected/2-2020.txt')


# --------------------------------------------------
def test_4_2020() -> None:
    """ April 2020 """

    run_test(['-m', '4', '2020'], 'tests/expected/4-2020.txt')


# --------------------------------------------------
def test_april_2020() -> None:
    """ April 2020 by name """

    run_test(['2020', '-m', 'april'], 'tests/expected/4-2020.txt')


# --------------------------------------------------
def test_2020() -> None:
    """ Full year 2020 """

    run_test(['2020'], 'tests/expected/2020.txt')


# --------------------------------------------------
def test_year() -> None:
    """ Current year with -y """

    res = run([PRG, '-y'], capture_output=True, text=True)
    assert res.returncode == 0
    lines = res.stdout.split('\n')
    assert len(lines) == 37
