init:
	apt update && apt install --auto-remove -y lcov python3-venv python3-pip python3-dev python3-setuptools 
	python3 -m venv venv
	. venv/bin/activate
	pip install .
test:
	pytest --cov-report term-missing --cov-report lcov:./tests/lcov/cov.info --cov=mm tests
	genhtml ./tests/lcov/cov.info -o ./tests/lcov/html
package:
	python3 -m pip install --upgrade build
	python3 -m build
	
.PHONY: init test package
