.PHONY: help install test lint format clean docker-build docker-run notebooks reports

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  clean       - Clean temporary files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run Docker container"
	@echo "  notebooks   - Test notebooks"
	@echo "  reports     - Generate reports"
	@echo "  validate    - Validate data"

# Installation
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	python scripts/setup_environment.py

# Testing
test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-fast:
	pytest tests/ -v -x

# Code quality
lint:
	flake8 src/ tests/ scripts/
	mypy src/ --ignore-missing-imports

format:
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

# Cleaning
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/
	rm -rf build/ dist/

# Docker
docker-build:
	docker build -t portfolio-optimization .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

# Analysis
notebooks:
	python scripts/test_notebooks.py

reports:
	python scripts/generate_reports.py

validate:
	python scripts/validate_data.py

# Development
dev-setup: install
	pre-commit install
	@echo "Development environment ready!"

# Production
prod-setup:
	pip install -r requirements.txt
	python scripts/setup_environment.py --production

# Backup
backup:
	tar -czf backup_$(shell date +%Y%m%d_%H%M%S).tar.gz \
		src/ notebooks/ scripts/ config/ data/ models/

# Documentation
docs:
	cd docs && make html

# All-in-one commands
full-test: lint test notebooks validate
	@echo "All tests completed successfully!"

deploy-prep: clean format lint test
	@echo "Ready for deployment!"
