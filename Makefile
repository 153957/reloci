.PHONY: flaketest unittests dist

flaketest:
	flake8

unittests:
	python -m unittest discover --catch --start-directory tests --top-level-directory .

dist:
	python -m build --sdist --wheel
