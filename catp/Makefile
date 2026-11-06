.PHONY: test

PRG = catp.py

test:
	uv run pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy $(PRG) tests/test_catp.py

all:
	../bin/all_test.py $(PRG)
