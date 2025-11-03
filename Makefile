.PHONY: help install test coverage build clean format check-format lint precommit update-submodules

.DEFAULT_GOAL := help

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

install: update-submodules ## Install development dependencies
	pip install -e '.[dev]'

update-submodules: ## Update all git submodules
	git submodule sync --recursive
	git submodule update --init --remote --recursive

test: ## Run test suite
	python -m unittest discover -s src/ -v

coverage: ## Generate coverage report
	coverage run -m unittest discover
	coverage report
	coverage xml

build: ## Build source and wheel distributions
	python -m build

clean: ## Remove build artifacts and temporary files
	rm -rf build/ dist/ *.egg-info/ **/*.egg-info/ .coverage coverage.xml .mypy_cache/ 88

format: ## Auto-format code with isort and black
	isort .
	black .

check-format: ## Check code formatting with isort and black
	isort --check-only --diff .
	black --check --diff .

lint: ## Run all code quality checks
	flake8 --config=flake8.ini .
	mypy src/ --install-types --non-interactive

precommit: format lint ## Full pre-commit checks (format + lint)

##@ Development Targets
