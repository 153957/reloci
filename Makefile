.PHONY: ruffinstall
ruffinstall:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager -r requirements-ruff.txt

.PHONY: devinstall
devinstall:
	pip install --upgrade pip
	pip install --upgrade --upgrade-strategy eager --editable .[dev]

.PHONY: test
test: rufftest typingtest unittests

.PHONY: rufftest
rufftest:
	ruff check .
	ruff format --check .

.PHONY: typingtest
typingtest:
	mypy .

.PHONY: unittests
unittests:
	python -m unittest discover --catch --start-directory tests --top-level-directory .

.PHONY: clean
clean:
	rm -rf dist

.PHONY: publish
publish:
	flit publish

.PHONY: demo
demo:
	make -C demo/ demo
