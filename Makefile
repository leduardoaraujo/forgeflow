.PHONY: install dev test run clean format lint

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

run:
	uvicorn dataforge.api.main:app --reload --host 0.0.0.0 --port 8000

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ htmlcov/ .coverage

format:
	ruff format dataforge/ tests/

lint:
	ruff check dataforge/ tests/
