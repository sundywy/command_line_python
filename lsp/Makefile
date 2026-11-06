.PHONY: test

PRG = lsp.py

test:
	./set-test-perms.sh
	uv run pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy $(PRG) tests/test_lsp.py

all:
	../bin/all_test.py $(PRG)
