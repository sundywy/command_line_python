.PHONY: test

PRG = commp.py

test:
	# uv run pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy $(PRG) tests/test_commp.py
	uv run pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc $(PRG) tests/test_commp.py

all:
	../bin/all_test.py $(PRG)
