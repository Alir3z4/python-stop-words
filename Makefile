.PHONY: install test build release clean

install: update_stop_words
	pip install '.[dev]'
	pip install build

update_stop_words:
	git submodule update --remote --rebase

test:
	python -m unittest discover

coverage:
	coverage run -m unittest discover
	coverage report
	coverage xml

build:
	python -m build

clean:
	rm -rf dist *.egg-info coverage.xml build .coverage

lint:
	black stop_words/
	flake8 stop_words/ --config flake8.ini
	mypy stop_words/ --install-types --non-interactive
