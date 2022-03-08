install:
	poetry install

lint:
	poetry run flake8 page_loader
	poetry run flake8 tests

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

publish:
	poetry publish --dry-run

test:
	poetry run pytest -vv

test-coverage:
	poetry run pytest --cov=page_loader tests --cov-report xml

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build
