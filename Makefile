.PHONY: test
test: rufftest typingtest unittests

.PHONY: rufftest
rufftest:
	uv run ruff check .
	uv run ruff format --check .

.PHONY: typingtest
typingtest:
	uv run ty check

.PHONY: unittests
unittests:
	uv run python -m unittest discover --catch --start-directory tests --top-level-directory .

.PHONY: clean
clean:
	rm -rf dist

.PHONY: publish
publish:
	uv build
	uv publish

.PHONY: demo
demo:
	make -C demo/ demo
