GUNICORN=$(VIRTUAL_ENV)/bin/gunicorn
MANAGE_PY=$(VIRTUAL_ENV)/bin/python manage.py
COVERAGE=$(VIRTUAL_ENV)/bin/coverage run
PIP=$(VIRTUAL_ENV)/bin/pip

SETTINGS_DEV=comfortbus.settings.dev
SETTINGS_TEST=comfortbus.settings.test
SETTINGS_PROD=comfortbus.settings.prod

.PHONY: all check.venv check.settings dev prod requirements super shell clean runserver gunicorn db migrate makemig static test

all: help

help:
	@echo 'Makefile *** alpha *** Makefile'

check.venv:
	@if test "$(VIRTUAL_ENV)" = "" ; then echo "VIRTUAL_ENV is undefined"; exit 1; fi

check.settings:
	@if test "$(SETTINGS)" = "" ; then echo "SETTINGS is undefined"; exit 1; fi

dev: check.venv
	$(eval SETTINGS:=$(SETTINGS_DEV))

prod: check.venv
	$(eval SETTINGS:=$(SETTINGS_PROD))

requirements: check.venv
	@$(PIP) install -r requirements.txt

super: check.settings
	@$(MANAGE_PY) createsuperuser --settings=$(SETTINGS)

shell: check.settings
	@$(MANAGE_PY) shell --settings=$(SETTINGS)

clean:
	@find . -name '*.pyc' -exec rm -f {} \;
	@find . -name 'Thumbs.db' -exec rm -f {} \;
	@find . -name '*~' -exec rm -f {} \;

runserver: check.settings
	@$(MANAGE_PY) runserver --settings=$(SETTINGS)

gunicorn: check.settings
	@$(GUNICORN) comfortbus.wsgi -w 4 -b 127.0.0.1:8000 --settings=$(SETTINGS)

db: check.settings makemig migrate

migrate: check.settings
	@$(MANAGE_PY) migrate --noinput --settings=$(SETTINGS)

makemig: check.settings
	@$(MANAGE_PY) makemigrations --settings=$(SETTINGS)

static: check.settings
	@$(MANAGE_PY) collectstatic --clear --noinput --settings=$(SETTINGS)

tests:
	@$(MANAGE_PY) test --settings=$(SETTINGS_TEST)

test:
	@$(MANAGE_PY) test $(INPUT) --settings=$(SETTINGS_TEST)

coverage:
	@$(COVERAGE) --source=$(INPUT) manage.py test --settings=$(SETTINGS_TEST)
