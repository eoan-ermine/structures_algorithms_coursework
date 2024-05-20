CODE = structures_algorithms_coursework

all:
	@echo "make devenv		- Create & setup development virtual environment"
	@echo "make lint		- Check code with pylint"
	@echo "make format		- Format code with pre-commit hooks"
	@echo "make clean		- Remove files created by distutils"
	@echo "make sdist		- Make source distribution"
	@exit 0

clean:
	rm -rf dist

devenv: clean
	rm -rf `poetry env info -p`
	poetry install
	poetry run pre-commit install

lint:
	poetry run pylint $(CODE)

format:
	poetry run pre-commit run --all-files

sdist: clean
	poetry build
