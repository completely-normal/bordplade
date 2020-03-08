.PHONY: \
	help \
	build \
	build-frontend \
	build-backend \
	env-test \
	env-setup \
 	env-update \
 	container-deploy \
 	container-teardown

.DEFAULT: help

THIS_MAKEFILE := $(lastword $(MAKEFILE_LIST))

# The ``SHELL`` override enables us to use bash and add some customization to the make-environment.
SHELL := PYENV_VIRTUALENVS_IN_PROJECT=true /bin/bash
SHELL := /bin/bash

help:
	## Displays some notes for how to use the makefile.
	# TODO

pyproject.lock:
	poetry lock

requirements.txt: pyproject.lock
	poetry run pip freeze > $@

build:  build-frontend build-backend
	## invokes both `build-frontend` and `build-backend`

build-frontend:
	yarn run build
	@ln -s frontend/build/ backend/src/bordplade_frontend/static/

build-backend:
	## Build a distributable package, which can then be found in the `dist/` directory.
	poetry run isort backend/**/*.py
	poetry build --format wheel

env-setup:
	poetry init

env-update:
	poetry update

container-deploy: requirements.txt
	docker-compose \
		-f deploy/docker-compose.yml \
		--project-name bordplade \
		up

container-teardown:
	docker-compose \
		-f deploy/docker-compose.yml \
		--project-name bordplade \
		down

run-devserver:
	DJANGO_SETTINGS_MODULE="bordplade.settings.dev" poetry run backend/src/boardplade/manage.py runserver
