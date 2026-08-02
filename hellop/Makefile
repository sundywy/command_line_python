.PHONY: test

test:
	python3 -m pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy hellop.py truep.py falsep.py tests/test_hellop.py

all:
	../bin/all_test.py hellop
