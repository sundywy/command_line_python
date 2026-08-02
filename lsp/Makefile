.PHONY: test

PRG = lsp.py

test:
	./set-test-perms.sh
	python3 -m pytest -xv --flake8 --pylint --pylint-rcfile=../pylintrc --mypy $(PRG) tests/test_lsp.py

all:
	../bin/all_test.py $(PRG)
