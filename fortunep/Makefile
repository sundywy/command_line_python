.PHONY: test

PRG = fortunep.py

test:
	uv run pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy $(PRG) tests/test_fortunep.py

all:
	../bin/all_test.py $(PRG)
