.PHONY: all

# Help menu on a naked make
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

fmt: ## (Format) - runs black and isort against the codebase
	poetry run black ./dpytools/*
	poetry run isort ./dpytools/*

lint: ## Run the ruff python linter
	poetry run ruff ./dpytools/*

test: ## Run pytest and check test coverage
	poetry run pytest --cov-report term-missing --cov=dpytools
