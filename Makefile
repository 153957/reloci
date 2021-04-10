.PHONY: test dist

test:
	flake8

dist:
	python -m build --sdist --wheel
