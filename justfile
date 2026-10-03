[parallel]
test: lint typingtest coveragetest

lint:
    uv run ruff check .
    uv run ruff format --check .

lintfix:
    uv run ruff check --fix-only .
    uv run ruff format .
    uv run ruff check --fix-only .
    uv run ruff format .

typingtest:
    uv run ty check --no-progress .

unittests:
    uv run coverage run -m unittest --durations 5

coveragetest: unittests
    uv run coverage report

clean:
    rm -rf dist

publish:
    uv build
    uv publish

demo:
    just demo/demo
