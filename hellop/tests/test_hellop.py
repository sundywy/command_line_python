""" Tests for hellop """

import os
from subprocess import getstatusoutput, run

HELLO: str = './hellop.py'
TRUE: str = './truep.py'
FALSE: str = './falsep.py'


# --------------------------------------------------
def test_exists() -> None:
    """ Programs exist """

    assert os.path.isfile(HELLO)
    assert os.path.isfile(TRUE)
    assert os.path.isfile(FALSE)


# --------------------------------------------------
def test_hello_runs() -> None:
    """ hello prints Hello, world! """

    res = run([HELLO], capture_output=True, text=True)
    assert res.returncode == 0
    assert res.stdout == 'Hello, world!\n'


# --------------------------------------------------
def test_true_ok() -> None:
    """ true exits successfully """

    rv, _ = getstatusoutput(TRUE)
    assert rv == 0


# --------------------------------------------------
def test_false_not_ok() -> None:
    """ false exits with failure """

    rv, _ = getstatusoutput(FALSE)
    assert rv != 0
