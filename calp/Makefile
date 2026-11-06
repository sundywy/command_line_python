.PHONY: test

PRG = calp.py

test:
	uv run pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy $(PRG) tests/test_calp.py

all:
	../bin/all_test.py $(PRG)
