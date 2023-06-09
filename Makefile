install:
	poetry install

update:
	poetry update

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest

reporter:
	coverage report -m

test-cov:
	poetry run pytest --cov-report xml --cov=page_analyzer tests/  

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app