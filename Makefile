install:
	poetry install

update:
	poetry update

build:
	poetry build 

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-uninstall:
	python3 -m pip uninstall dist/*.whl

package-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest

reporter:
	coverage report -m

test-cov:
	poetry run pytest --cov-report xml --cov=gendiff tests/  

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app