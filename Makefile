.PHONY: install test lint run up down seed
install:
	python -m pip install -e ".[dev]"
	playwright install chromium
test:
	pytest --cov=app --cov-report=term-missing
lint:
	ruff check .
run:
	uvicorn app.main:app --reload
up:
	docker compose up --build
down:
	docker compose down
seed:
	python -m scripts.seed
