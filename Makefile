.PHONY: test
test: rufftest typingtest coveragetest

.PHONY: rufftest
rufftest:
	uv run ruff check .
	uv run ruff format --check .

.PHONY: rufffix
rufffix:
	uv run ruff check --fix-only .
	uv run ruff format .

.PHONY: typingtest
typingtest:
	uv run ty check

.PHONY: unittests
unittests:
	uv run coverage run -m unittest --durations 5

.PHONY: coveragetest
coveragetest: unittests
	uv run coverage report

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
