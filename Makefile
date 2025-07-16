.PHONY: format
format:
	ruff format
	ruff check --fix .
	ruff format

.PHONY: static
static:
	mypy src
