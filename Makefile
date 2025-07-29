TOKEN ?= ""

.PHONY: format
format:
	uv run ruff format
	uv run ruff check --fix .
	uv run ruff format

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: static
static:
	uv run mypy src

.PHONY: build
build:
	uv run python -m build

.PHONY: release
release:
	uv run twine upload --repository pypi dist/* -u __token__ --password "${TOKEN}"

.PHONY: test
test:
	uv run pytest
