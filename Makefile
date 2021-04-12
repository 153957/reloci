.PHONY: flaketest unittests dist install

flaketest:
	flake8

unittests:
	python -m unittest discover --catch --start-directory tests --top-level-directory .

dist:
	python -m build --sdist --wheel

install:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager --editable .[test]
