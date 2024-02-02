init:
	pip install -r requirements.txt
	apt update && apt install --auto-remove -y lcov

test:
	pytest --cov-report lcov:./tests/lcov/cov.info --cov=mmdiagram tests
	genhtml ./tests/lcov/cov.info -o ./tests/lcov/html

.PHONY: init test