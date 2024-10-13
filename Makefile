py = $$(if [ -d $(PWD)/'.venv' ]; then echo $(PWD)/".venv/bin/python3"; else echo "python3"; fi)
pip = $(py) -m pip

test-makefile: ## Test makefile
	@echo "Test makefile done" > test-makefile.txt
	@cat test-makefile.txt
	@rm test-makefile.txt

.PHONY: help
help: ## Show this help
	@echo "Usage: make [target], targets are:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: setup-dev
setup-dev: ## setup dev environment: uv sync and .env
	uv sync --frozen --dev
	[ ! -e ".env" ] && cp ".env.example" ".env" || echo "file .env already exists"


.PHONY: update-pre-commit
update-pre-commit: ## Update pre-commit hooks
	pre-commit autoupdate


.PHONY: run-separate
run-separate: ## Run docker-compose in detached mode
	docker-compose -f docker-compose.yaml up --detach

.PHONY: run
run: ## Run docker-compose in detached mode
	docker-compose -f docker-compose.yaml up --detach

.PHONY: stop
stop: ## Stop docker-compose
	docker-compose down

.PHONY: build
build: purge ## Build docker-compose from scratch
	docker-compose build

.PHONY: purge
purge: ## Purge docker-compose
	docker-compose down --remove-orphans

.PHONY: logs
logs: ## Show docker-compose logs
	docker-compose logs --timestamps --follow

.PHONY: test-units
test-units: ## Run pytest
	docker-compose --env-file ".env" run  --no-deps --rm api pytest tests/units


.PHONY: test-integration
test-integration: ## Run integration tests
	docker-compose --env-file ".env" run  --no-deps --rm api pytest tests/integration


.PHONY: test-all
test-all: ## Run all tests
	docker-compose --env-file ".env" run  --no-deps --rm api pytest

.PHONY: coverage
coverage: ## Run coverage
	docker-compose --env-file ".env" run  --no-deps --rm api pytest --cov

.PHONY: makemigrations
makemigrations: ## Run makemigrations
	docker exec -it api alembic revision --autogenerate


.PHONY: migrate
migrate: ## Run migrate
	docker exec -it api alembic upgrade head

.PHONY: access-db
access-db: ## Access database
	docker exec -it database psql "example-db" -U "example-user"
