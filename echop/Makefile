.PHONY: test

test:
	uv run pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy echop.py tests/test_echop.py

all:
	../bin/all_test.py echop
