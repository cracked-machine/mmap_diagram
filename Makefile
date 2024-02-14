init:
	sudo apt update && sudo apt install --auto-remove -y lcov python3-venv python3-pip python3-dev python3-setuptools 
	python3 -m venv venv
	. venv/bin/activate && pip install .
test:
	. venv/bin/activate && pytest --cov-report term-missing --cov-report lcov:./tests/lcov/cov.info --cov=mm tests
	genhtml ./tests/lcov/cov.info -o ./tests/lcov/html
pkg:
	python3 -m pip install --upgrade build
	python3 -m build
	
.PHONY: init test pkg
