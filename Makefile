.PHONY: ruffinstall
ruffinstall:
	uv pip install --upgrade -r requirements-ruff.txt

.PHONY: devinstall
devinstall:
	uv pip install --upgrade --editable .[dev]

.PHONY: test
test: rufftest typingtest unittests

.PHONY: rufftest
rufftest:
	ruff check .
	ruff format --check .

.PHONY: typingtest
typingtest:
	ty check

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
