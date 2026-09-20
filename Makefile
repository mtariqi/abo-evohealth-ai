.PHONY: install demo test lint check

install:
	python -m pip install -e ".[dev]"

demo:
	abo-evohealth demo --config configs/demo.yaml

test:
	pytest

lint:
	ruff check .

check: lint test

