init:
	apt update && apt install --auto-remove -y lcov python3-venv python3-pip python3-dev python3-setuptools 
	python3 -m venv venv
	ls -la venv
	ls -la venv/bin
	pwd
	. venv/bin/activate
	pip install -r requirements.txt
test:
	pytest --cov-report term-missing --cov-report lcov:./tests/lcov/cov.info --cov=mm tests
	genhtml ./tests/lcov/cov.info -o ./tests/lcov/html

.PHONY: init test
