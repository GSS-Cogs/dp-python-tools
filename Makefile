.PHONY: all

# Help menu on a naked make
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

fmt: ## (Format) - runs black and isort against the codebase (auto triggered on pre-commit)
	pipenv run black ./src/*
	pipenv run isort ./src/*

lint: ## Run the ruff python linter (auto triggered on pre-commit)
	pipenv run ruff ./src/*

test: ## Run pytest and check test coverage (auto triggered on pre-push)
	pipenv run pytest --cov-report term-missing --cov=src --cov-config=./tests/coverage.rc
