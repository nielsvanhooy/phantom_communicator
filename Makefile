
.DEFAULT_GOAL := all

toml_sort:
	toml-sort pyproject.toml --all --in-place

isort:
	poetry run isort phantom_communicator

black:
	poetry run black phantom_communicator

flake8:
	poetry run flake8 phantom_communicator

pylint:
	poetry run pylint --recursive=true phantom_communicator

dockerfile_linter:
	docker run --rm -i hadolint/hadolint < Dockerfile

create_mypy_cache:
	bash -c "mkdir -p .mypy_cache"

mypy:
	poetry run mypy --install-types --non-interactive .

audit_dependencies:
	poetry export --without-hashes -f requirements.txt | poetry run safety check --full-report --stdin

bandit:
	poetry run bandit -r . -x ./bifrost/tests,./test,./tests

run_tests:
	poetry run pytest -o addopts='--cov=bifrost -p no:cacheprovider -vv  --doctest-modules --doctest-glob=*.md' .


lint: create_mypy_cache toml_sort isort black flake8 pylint mypy

audit: audit_dependencies bandit

tests: run_tests

all: lint audit tests

