""" Tests for tailp """

import os
import platform
import random
import re
import string
from subprocess import getstatusoutput, run
from typing import List

PRG: str = './tailp.py'
RUN: str = f'python {PRG}' if platform.system() == 'Windows' else PRG
EMPTY: str = 'tests/inputs/empty.txt'
ONE: str = 'tests/inputs/one.txt'
TWO: str = 'tests/inputs/two.txt'
THREE: str = 'tests/inputs/three.txt'
TWELVE: str = 'tests/inputs/twelve.txt'


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
def test_dies_bad_bytes() -> None:
    """ Dies on bad byte count """

    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} -c {bad} {EMPTY}')
    assert rv != 0
    assert f'illegal byte count -- {bad}' in out


# --------------------------------------------------
def test_dies_bad_lines() -> None:
    """ Dies on bad line count """

    bad = random_string()
    rv, out = getstatusoutput(f'{RUN} -n {bad} {EMPTY}')
    assert rv != 0
    assert f'illegal line count -- {bad}' in out


# --------------------------------------------------
def test_dies_bytes_and_lines() -> None:
    """ Dies when both -n and -c are used """

    rv, out = getstatusoutput(f'{RUN} -n 1 -c 2 {EMPTY}')
    assert rv != 0
    assert out.lower().startswith('usage')


# --------------------------------------------------
def test_skips_bad_file() -> None:
    """ Warns on bad file """

    bad = gen_bad_file()
    res = run([PRG, ONE, bad, TWO], capture_output=True, text=True)
    assert re.search(f'{bad}: .*No such file or directory', res.stderr)


# --------------------------------------------------
def run_test(args: List[str], expected_file: str) -> None:
    """ Test with input """

    assert os.path.isfile(expected_file)
    expected = open(expected_file, 'rb').read().decode('utf-8', 'replace')

    res = run([PRG] + args, capture_output=True)
    assert res.returncode == 0
    assert res.stdout.decode('utf-8', 'replace') == expected


# --------------------------------------------------

# --------------------------------------------------
def test_empty() -> None:
    """ empty """

    run_test([EMPTY], 'tests/expected/empty.txt.out')

# --------------------------------------------------
def test_empty_n0() -> None:
    """ empty_n0 """

    run_test([EMPTY, '-n', '0'], 'tests/expected/empty.txt.n0.out')

# --------------------------------------------------
def test_empty_n1() -> None:
    """ empty_n1 """

    run_test([EMPTY, '-n', '1'], 'tests/expected/empty.txt.n1.out')

# --------------------------------------------------
def test_empty_n_minus_1() -> None:
    """ empty_n_minus_1 """

    run_test([EMPTY, '-n=-1'], 'tests/expected/empty.txt.n1.out')

# --------------------------------------------------
def test_empty_n3() -> None:
    """ empty_n3 """

    run_test([EMPTY, '-n', '3'], 'tests/expected/empty.txt.n3.out')

# --------------------------------------------------
def test_empty_n_minus_3() -> None:
    """ empty_n_minus_3 """

    run_test([EMPTY, '-n=-3'], 'tests/expected/empty.txt.n3.out')

# --------------------------------------------------
def test_empty_n4() -> None:
    """ empty_n4 """

    run_test([EMPTY, '-n', '4'], 'tests/expected/empty.txt.n4.out')

# --------------------------------------------------
def test_empty_n_minus_4() -> None:
    """ empty_n_minus_4 """

    run_test([EMPTY, '-n=-4'], 'tests/expected/empty.txt.n4.out')

# --------------------------------------------------
def test_empty_n200() -> None:
    """ empty_n200 """

    run_test([EMPTY, '-n', '200'], 'tests/expected/empty.txt.n200.out')

# --------------------------------------------------
def test_empty_n_minus_200() -> None:
    """ empty_n_minus_200 """

    run_test([EMPTY, '-n=-200'], 'tests/expected/empty.txt.n200.out')

# --------------------------------------------------
def test_empty_n_plus_0() -> None:
    """ empty_n_plus_0 """

    run_test([EMPTY, '-n', '+0'], 'tests/expected/empty.txt.n+0.out')

# --------------------------------------------------
def test_empty_n_plus_1() -> None:
    """ empty_n_plus_1 """

    run_test([EMPTY, '-n', '+1'], 'tests/expected/empty.txt.n+1.out')

# --------------------------------------------------
def test_empty_n_plus_2() -> None:
    """ empty_n_plus_2 """

    run_test([EMPTY, '-n', '+2'], 'tests/expected/empty.txt.n+2.out')

# --------------------------------------------------
def test_empty_c3() -> None:
    """ empty_c3 """

    run_test([EMPTY, '-c', '3'], 'tests/expected/empty.txt.c3.out')

# --------------------------------------------------
def test_empty_c_minus_3() -> None:
    """ empty_c_minus_3 """

    run_test([EMPTY, '-c=-3'], 'tests/expected/empty.txt.c3.out')

# --------------------------------------------------
def test_empty_c8() -> None:
    """ empty_c8 """

    run_test([EMPTY, '-c', '8'], 'tests/expected/empty.txt.c8.out')

# --------------------------------------------------
def test_empty_c_minus_8() -> None:
    """ empty_c_minus_8 """

    run_test([EMPTY, '-c=8'], 'tests/expected/empty.txt.c8.out')

# --------------------------------------------------
def test_empty_c12() -> None:
    """ empty_c12 """

    run_test([EMPTY, '-c', '12'], 'tests/expected/empty.txt.c12.out')

# --------------------------------------------------
def test_empty_c_minus_12() -> None:
    """ empty_c_minus_12 """

    run_test([EMPTY, '-c=-12'], 'tests/expected/empty.txt.c12.out')

# --------------------------------------------------
def test_empty_c200() -> None:
    """ empty_c200 """

    run_test([EMPTY, '-c', '200'], 'tests/expected/empty.txt.c200.out')

# --------------------------------------------------
def test_empty_c_minus_200() -> None:
    """ empty_c_minus_200 """

    run_test([EMPTY, '-c=-200'], 'tests/expected/empty.txt.c200.out')

# --------------------------------------------------
def test_empty_c_plus_0() -> None:
    """ empty_c_plus_0 """

    run_test([EMPTY, '-c', '+0'], 'tests/expected/empty.txt.c+0.out')

# --------------------------------------------------
def test_empty_c_plus_1() -> None:
    """ empty_c_plus_1 """

    run_test([EMPTY, '-c', '+1'], 'tests/expected/empty.txt.c+1.out')

# --------------------------------------------------
def test_empty_c_plus_2() -> None:
    """ empty_c_plus_2 """

    run_test([EMPTY, '-c', '+2'], 'tests/expected/empty.txt.c+2.out')

# --------------------------------------------------

# --------------------------------------------------
def test_one() -> None:
    """ one """

    run_test([ONE], 'tests/expected/one.txt.out')

# --------------------------------------------------
def test_one_n0() -> None:
    """ one_n0 """

    run_test([ONE, '-n', '0'], 'tests/expected/one.txt.n0.out')

# --------------------------------------------------
def test_one_n1() -> None:
    """ one_n1 """

    run_test([ONE, '-n', '1'], 'tests/expected/one.txt.n1.out')

# --------------------------------------------------
def test_one_n_minus_1() -> None:
    """ one_n_minus_1 """

    run_test([ONE, '-n=-1'], 'tests/expected/one.txt.n1.out')

# --------------------------------------------------
def test_one_n3() -> None:
    """ one_n3 """

    run_test([ONE, '-n', '3'], 'tests/expected/one.txt.n3.out')

# --------------------------------------------------
def test_one_n_minus_3() -> None:
    """ one_n_minus_3 """

    run_test([ONE, '-n=-3'], 'tests/expected/one.txt.n3.out')

# --------------------------------------------------
def test_one_n4() -> None:
    """ one_n4 """

    run_test([ONE, '-n', '4'], 'tests/expected/one.txt.n4.out')

# --------------------------------------------------
def test_one_n_minus_4() -> None:
    """ one_n_minus_4 """

    run_test([ONE, '-n=-4'], 'tests/expected/one.txt.n4.out')

# --------------------------------------------------
def test_one_n200() -> None:
    """ one_n200 """

    run_test([ONE, '-n', '200'], 'tests/expected/one.txt.n200.out')

# --------------------------------------------------
def test_one_n_minus_200() -> None:
    """ one_n_minus_200 """

    run_test([ONE, '-n=-200'], 'tests/expected/one.txt.n200.out')

# --------------------------------------------------
def test_one_n_plus_0() -> None:
    """ one_n_plus_0 """

    run_test([ONE, '-n', '+0'], 'tests/expected/one.txt.n+0.out')

# --------------------------------------------------
def test_one_n_plus_1() -> None:
    """ one_n_plus_1 """

    run_test([ONE, '-n', '+1'], 'tests/expected/one.txt.n+1.out')

# --------------------------------------------------
def test_one_n_plus_2() -> None:
    """ one_n_plus_2 """

    run_test([ONE, '-n', '+2'], 'tests/expected/one.txt.n+2.out')

# --------------------------------------------------
def test_one_c3() -> None:
    """ one_c3 """

    run_test([ONE, '-c', '3'], 'tests/expected/one.txt.c3.out')

# --------------------------------------------------
def test_one_c_minus_3() -> None:
    """ one_c_minus_3 """

    run_test([ONE, '-c=-3'], 'tests/expected/one.txt.c3.out')

# --------------------------------------------------
def test_one_c8() -> None:
    """ one_c8 """

    run_test([ONE, '-c', '8'], 'tests/expected/one.txt.c8.out')

# --------------------------------------------------
def test_one_c_minus_8() -> None:
    """ one_c_minus_8 """

    run_test([ONE, '-c=8'], 'tests/expected/one.txt.c8.out')

# --------------------------------------------------
def test_one_c12() -> None:
    """ one_c12 """

    run_test([ONE, '-c', '12'], 'tests/expected/one.txt.c12.out')

# --------------------------------------------------
def test_one_c_minus_12() -> None:
    """ one_c_minus_12 """

    run_test([ONE, '-c=-12'], 'tests/expected/one.txt.c12.out')

# --------------------------------------------------
def test_one_c200() -> None:
    """ one_c200 """

    run_test([ONE, '-c', '200'], 'tests/expected/one.txt.c200.out')

# --------------------------------------------------
def test_one_c_minus_200() -> None:
    """ one_c_minus_200 """

    run_test([ONE, '-c=-200'], 'tests/expected/one.txt.c200.out')

# --------------------------------------------------
def test_one_c_plus_0() -> None:
    """ one_c_plus_0 """

    run_test([ONE, '-c', '+0'], 'tests/expected/one.txt.c+0.out')

# --------------------------------------------------
def test_one_c_plus_1() -> None:
    """ one_c_plus_1 """

    run_test([ONE, '-c', '+1'], 'tests/expected/one.txt.c+1.out')

# --------------------------------------------------
def test_one_c_plus_2() -> None:
    """ one_c_plus_2 """

    run_test([ONE, '-c', '+2'], 'tests/expected/one.txt.c+2.out')

# --------------------------------------------------

# --------------------------------------------------
def test_two() -> None:
    """ two """

    run_test([TWO], 'tests/expected/two.txt.out')

# --------------------------------------------------
def test_two_n0() -> None:
    """ two_n0 """

    run_test([TWO, '-n', '0'], 'tests/expected/two.txt.n0.out')

# --------------------------------------------------
def test_two_n1() -> None:
    """ two_n1 """

    run_test([TWO, '-n', '1'], 'tests/expected/two.txt.n1.out')

# --------------------------------------------------
def test_two_n_minus_1() -> None:
    """ two_n_minus_1 """

    run_test([TWO, '-n=-1'], 'tests/expected/two.txt.n1.out')

# --------------------------------------------------
def test_two_n3() -> None:
    """ two_n3 """

    run_test([TWO, '-n', '3'], 'tests/expected/two.txt.n3.out')

# --------------------------------------------------
def test_two_n_minus_3() -> None:
    """ two_n_minus_3 """

    run_test([TWO, '-n=-3'], 'tests/expected/two.txt.n3.out')

# --------------------------------------------------
def test_two_n4() -> None:
    """ two_n4 """

    run_test([TWO, '-n', '4'], 'tests/expected/two.txt.n4.out')

# --------------------------------------------------
def test_two_n_minus_4() -> None:
    """ two_n_minus_4 """

    run_test([TWO, '-n=-4'], 'tests/expected/two.txt.n4.out')

# --------------------------------------------------
def test_two_n200() -> None:
    """ two_n200 """

    run_test([TWO, '-n', '200'], 'tests/expected/two.txt.n200.out')

# --------------------------------------------------
def test_two_n_minus_200() -> None:
    """ two_n_minus_200 """

    run_test([TWO, '-n=-200'], 'tests/expected/two.txt.n200.out')

# --------------------------------------------------
def test_two_n_plus_0() -> None:
    """ two_n_plus_0 """

    run_test([TWO, '-n', '+0'], 'tests/expected/two.txt.n+0.out')

# --------------------------------------------------
def test_two_n_plus_1() -> None:
    """ two_n_plus_1 """

    run_test([TWO, '-n', '+1'], 'tests/expected/two.txt.n+1.out')

# --------------------------------------------------
def test_two_n_plus_2() -> None:
    """ two_n_plus_2 """

    run_test([TWO, '-n', '+2'], 'tests/expected/two.txt.n+2.out')

# --------------------------------------------------
def test_two_c3() -> None:
    """ two_c3 """

    run_test([TWO, '-c', '3'], 'tests/expected/two.txt.c3.out')

# --------------------------------------------------
def test_two_c_minus_3() -> None:
    """ two_c_minus_3 """

    run_test([TWO, '-c=-3'], 'tests/expected/two.txt.c3.out')

# --------------------------------------------------
def test_two_c8() -> None:
    """ two_c8 """

    run_test([TWO, '-c', '8'], 'tests/expected/two.txt.c8.out')

# --------------------------------------------------
def test_two_c_minus_8() -> None:
    """ two_c_minus_8 """

    run_test([TWO, '-c=8'], 'tests/expected/two.txt.c8.out')

# --------------------------------------------------
def test_two_c12() -> None:
    """ two_c12 """

    run_test([TWO, '-c', '12'], 'tests/expected/two.txt.c12.out')

# --------------------------------------------------
def test_two_c_minus_12() -> None:
    """ two_c_minus_12 """

    run_test([TWO, '-c=-12'], 'tests/expected/two.txt.c12.out')

# --------------------------------------------------
def test_two_c200() -> None:
    """ two_c200 """

    run_test([TWO, '-c', '200'], 'tests/expected/two.txt.c200.out')

# --------------------------------------------------
def test_two_c_minus_200() -> None:
    """ two_c_minus_200 """

    run_test([TWO, '-c=-200'], 'tests/expected/two.txt.c200.out')

# --------------------------------------------------
def test_two_c_plus_0() -> None:
    """ two_c_plus_0 """

    run_test([TWO, '-c', '+0'], 'tests/expected/two.txt.c+0.out')

# --------------------------------------------------
def test_two_c_plus_1() -> None:
    """ two_c_plus_1 """

    run_test([TWO, '-c', '+1'], 'tests/expected/two.txt.c+1.out')

# --------------------------------------------------
def test_two_c_plus_2() -> None:
    """ two_c_plus_2 """

    run_test([TWO, '-c', '+2'], 'tests/expected/two.txt.c+2.out')

# --------------------------------------------------

# --------------------------------------------------
def test_three() -> None:
    """ three """

    run_test([THREE], 'tests/expected/three.txt.out')

# --------------------------------------------------
def test_three_n0() -> None:
    """ three_n0 """

    run_test([THREE, '-n', '0'], 'tests/expected/three.txt.n0.out')

# --------------------------------------------------
def test_three_n1() -> None:
    """ three_n1 """

    run_test([THREE, '-n', '1'], 'tests/expected/three.txt.n1.out')

# --------------------------------------------------
def test_three_n_minus_1() -> None:
    """ three_n_minus_1 """

    run_test([THREE, '-n=-1'], 'tests/expected/three.txt.n1.out')

# --------------------------------------------------
def test_three_n3() -> None:
    """ three_n3 """

    run_test([THREE, '-n', '3'], 'tests/expected/three.txt.n3.out')

# --------------------------------------------------
def test_three_n_minus_3() -> None:
    """ three_n_minus_3 """

    run_test([THREE, '-n=-3'], 'tests/expected/three.txt.n3.out')

# --------------------------------------------------
def test_three_n4() -> None:
    """ three_n4 """

    run_test([THREE, '-n', '4'], 'tests/expected/three.txt.n4.out')

# --------------------------------------------------
def test_three_n_minus_4() -> None:
    """ three_n_minus_4 """

    run_test([THREE, '-n=-4'], 'tests/expected/three.txt.n4.out')

# --------------------------------------------------
def test_three_n200() -> None:
    """ three_n200 """

    run_test([THREE, '-n', '200'], 'tests/expected/three.txt.n200.out')

# --------------------------------------------------
def test_three_n_minus_200() -> None:
    """ three_n_minus_200 """

    run_test([THREE, '-n=-200'], 'tests/expected/three.txt.n200.out')

# --------------------------------------------------
def test_three_n_plus_0() -> None:
    """ three_n_plus_0 """

    run_test([THREE, '-n', '+0'], 'tests/expected/three.txt.n+0.out')

# --------------------------------------------------
def test_three_n_plus_1() -> None:
    """ three_n_plus_1 """

    run_test([THREE, '-n', '+1'], 'tests/expected/three.txt.n+1.out')

# --------------------------------------------------
def test_three_n_plus_2() -> None:
    """ three_n_plus_2 """

    run_test([THREE, '-n', '+2'], 'tests/expected/three.txt.n+2.out')

# --------------------------------------------------
def test_three_c3() -> None:
    """ three_c3 """

    run_test([THREE, '-c', '3'], 'tests/expected/three.txt.c3.out')

# --------------------------------------------------
def test_three_c_minus_3() -> None:
    """ three_c_minus_3 """

    run_test([THREE, '-c=-3'], 'tests/expected/three.txt.c3.out')

# --------------------------------------------------
def test_three_c8() -> None:
    """ three_c8 """

    run_test([THREE, '-c', '8'], 'tests/expected/three.txt.c8.out')

# --------------------------------------------------
def test_three_c_minus_8() -> None:
    """ three_c_minus_8 """

    run_test([THREE, '-c=8'], 'tests/expected/three.txt.c8.out')

# --------------------------------------------------
def test_three_c12() -> None:
    """ three_c12 """

    run_test([THREE, '-c', '12'], 'tests/expected/three.txt.c12.out')

# --------------------------------------------------
def test_three_c_minus_12() -> None:
    """ three_c_minus_12 """

    run_test([THREE, '-c=-12'], 'tests/expected/three.txt.c12.out')

# --------------------------------------------------
def test_three_c200() -> None:
    """ three_c200 """

    run_test([THREE, '-c', '200'], 'tests/expected/three.txt.c200.out')

# --------------------------------------------------
def test_three_c_minus_200() -> None:
    """ three_c_minus_200 """

    run_test([THREE, '-c=-200'], 'tests/expected/three.txt.c200.out')

# --------------------------------------------------
def test_three_c_plus_0() -> None:
    """ three_c_plus_0 """

    run_test([THREE, '-c', '+0'], 'tests/expected/three.txt.c+0.out')

# --------------------------------------------------
def test_three_c_plus_1() -> None:
    """ three_c_plus_1 """

    run_test([THREE, '-c', '+1'], 'tests/expected/three.txt.c+1.out')

# --------------------------------------------------
def test_three_c_plus_2() -> None:
    """ three_c_plus_2 """

    run_test([THREE, '-c', '+2'], 'tests/expected/three.txt.c+2.out')

# --------------------------------------------------

# --------------------------------------------------
def test_twelve() -> None:
    """ twelve """

    run_test([TWELVE], 'tests/expected/twelve.txt.out')

# --------------------------------------------------
def test_twelve_n0() -> None:
    """ twelve_n0 """

    run_test([TWELVE, '-n', '0'], 'tests/expected/twelve.txt.n0.out')

# --------------------------------------------------
def test_twelve_n1() -> None:
    """ twelve_n1 """

    run_test([TWELVE, '-n', '1'], 'tests/expected/twelve.txt.n1.out')

# --------------------------------------------------
def test_twelve_n_minus_1() -> None:
    """ twelve_n_minus_1 """

    run_test([TWELVE, '-n=-1'], 'tests/expected/twelve.txt.n1.out')

# --------------------------------------------------
def test_twelve_n3() -> None:
    """ twelve_n3 """

    run_test([TWELVE, '-n', '3'], 'tests/expected/twelve.txt.n3.out')

# --------------------------------------------------
def test_twelve_n_minus_3() -> None:
    """ twelve_n_minus_3 """

    run_test([TWELVE, '-n=-3'], 'tests/expected/twelve.txt.n3.out')

# --------------------------------------------------
def test_twelve_n4() -> None:
    """ twelve_n4 """

    run_test([TWELVE, '-n', '4'], 'tests/expected/twelve.txt.n4.out')

# --------------------------------------------------
def test_twelve_n_minus_4() -> None:
    """ twelve_n_minus_4 """

    run_test([TWELVE, '-n=-4'], 'tests/expected/twelve.txt.n4.out')

# --------------------------------------------------
def test_twelve_n200() -> None:
    """ twelve_n200 """

    run_test([TWELVE, '-n', '200'], 'tests/expected/twelve.txt.n200.out')

# --------------------------------------------------
def test_twelve_n_minus_200() -> None:
    """ twelve_n_minus_200 """

    run_test([TWELVE, '-n=-200'], 'tests/expected/twelve.txt.n200.out')

# --------------------------------------------------
def test_twelve_n_plus_0() -> None:
    """ twelve_n_plus_0 """

    run_test([TWELVE, '-n', '+0'], 'tests/expected/twelve.txt.n+0.out')

# --------------------------------------------------
def test_twelve_n_plus_1() -> None:
    """ twelve_n_plus_1 """

    run_test([TWELVE, '-n', '+1'], 'tests/expected/twelve.txt.n+1.out')

# --------------------------------------------------
def test_twelve_n_plus_2() -> None:
    """ twelve_n_plus_2 """

    run_test([TWELVE, '-n', '+2'], 'tests/expected/twelve.txt.n+2.out')

# --------------------------------------------------
def test_twelve_c3() -> None:
    """ twelve_c3 """

    run_test([TWELVE, '-c', '3'], 'tests/expected/twelve.txt.c3.out')

# --------------------------------------------------
def test_twelve_c_minus_3() -> None:
    """ twelve_c_minus_3 """

    run_test([TWELVE, '-c=-3'], 'tests/expected/twelve.txt.c3.out')

# --------------------------------------------------
def test_twelve_c8() -> None:
    """ twelve_c8 """

    run_test([TWELVE, '-c', '8'], 'tests/expected/twelve.txt.c8.out')

# --------------------------------------------------
def test_twelve_c_minus_8() -> None:
    """ twelve_c_minus_8 """

    run_test([TWELVE, '-c=8'], 'tests/expected/twelve.txt.c8.out')

# --------------------------------------------------
def test_twelve_c12() -> None:
    """ twelve_c12 """

    run_test([TWELVE, '-c', '12'], 'tests/expected/twelve.txt.c12.out')

# --------------------------------------------------
def test_twelve_c_minus_12() -> None:
    """ twelve_c_minus_12 """

    run_test([TWELVE, '-c=-12'], 'tests/expected/twelve.txt.c12.out')

# --------------------------------------------------
def test_twelve_c200() -> None:
    """ twelve_c200 """

    run_test([TWELVE, '-c', '200'], 'tests/expected/twelve.txt.c200.out')

# --------------------------------------------------
def test_twelve_c_minus_200() -> None:
    """ twelve_c_minus_200 """

    run_test([TWELVE, '-c=-200'], 'tests/expected/twelve.txt.c200.out')

# --------------------------------------------------
def test_twelve_c_plus_0() -> None:
    """ twelve_c_plus_0 """

    run_test([TWELVE, '-c', '+0'], 'tests/expected/twelve.txt.c+0.out')

# --------------------------------------------------
def test_twelve_c_plus_1() -> None:
    """ twelve_c_plus_1 """

    run_test([TWELVE, '-c', '+1'], 'tests/expected/twelve.txt.c+1.out')

# --------------------------------------------------
def test_twelve_c_plus_2() -> None:
    """ twelve_c_plus_2 """

    run_test([TWELVE, '-c', '+2'], 'tests/expected/twelve.txt.c+2.out')

# --------------------------------------------------

# --------------------------------------------------
def test_multiple_files() -> None:
    """ test_multiple_files """

    run_test([TWELVE, EMPTY, ONE, THREE, TWO], 'tests/expected/all.out')

# --------------------------------------------------
def test_multiple_files_n0() -> None:
    """ test_multiple_files_n0 """

    run_test(['-n', '0', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.n0.out')

# --------------------------------------------------
def test_multiple_files_n1() -> None:
    """ test_multiple_files_n1 """

    run_test(['-n', '1', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.n1.out')

# --------------------------------------------------
def test_multiple_files_n1_q() -> None:
    """ test_multiple_files_n1_q """

    run_test(['-n', '1', '-q', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.n1.q.out')

# --------------------------------------------------
def test_multiple_files_n1_quiet() -> None:
    """ test_multiple_files_n1_quiet """

    run_test(['-n', '1', '--quiet', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.n1.q.out')

# --------------------------------------------------
def test_multiple_files_n_minus_1() -> None:
    """ test_multiple_files_n_minus_1 """

    run_test(['-n=-1', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.n1.out')

# --------------------------------------------------
def test_multiple_files_n_plus_1() -> None:
    """ test_multiple_files_n_plus_1 """

    run_test(['-n', '+1', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.n+1.out')

# --------------------------------------------------
def test_multiple_files_n3() -> None:
    """ test_multiple_files_n3 """

    run_test(['-n', '3', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.n3.out')

# --------------------------------------------------
def test_multiple_files_n_minus_3() -> None:
    """ test_multiple_files_n_minus_3 """

    run_test(['-n=-3', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.n3.out')

# --------------------------------------------------
def test_multiple_files_n_plus_3() -> None:
    """ test_multiple_files_n_plus_3 """

    run_test(['-n', '+3', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.n+3.out')

# --------------------------------------------------
def test_multiple_files_c0() -> None:
    """ test_multiple_files_c0 """

    run_test(['-c', '0', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.c0.out')

# --------------------------------------------------
def test_multiple_files_c3() -> None:
    """ test_multiple_files_c3 """

    run_test(['-c', '3', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.c3.out')

# --------------------------------------------------
def test_multiple_files_c_minus_3() -> None:
    """ test_multiple_files_c_minus_3 """

    run_test(['-c=-3', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.c3.out')

# --------------------------------------------------
def test_multiple_files_c_plus_3() -> None:
    """ test_multiple_files_c_plus_3 """

    run_test(['-c', '+3', TWELVE, EMPTY, ONE, THREE, TWO],
             'tests/expected/all.c+3.out')
