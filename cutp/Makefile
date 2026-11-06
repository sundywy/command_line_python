.PHONY: test

PRG = cutp.py

test:
	uv run pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy $(PRG) tests/unit_test.py tests/test_cutp.py

all:
	../bin/all_test.py $(PRG)
