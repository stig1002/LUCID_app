.PHONY: clean format check install

clean:
	rm -rf */__pycache__/
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage

format: clean
	isort .
	black .
	make clean

check: clean
	isort . -c
	black . --check
	bandit .
	make clean

install: clean
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	make clean