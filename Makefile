init:
	pip install -r requirements.txt
	apt update && apt install --auto-remove -y lcov

test:
	pytest --cov-report term-missing --cov-report lcov:./tests/lcov/cov.info --cov=mm tests
	genhtml ./tests/lcov/cov.info -o ./tests/lcov/html

.PHONY: init test