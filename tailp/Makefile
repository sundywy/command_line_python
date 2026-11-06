.PHONY: test

PRG = tailp.py

test:
	uv run pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy $(PRG) tests/test_tailp.py

all:
	../bin/all_test.py $(PRG)
