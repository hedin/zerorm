test: flake8 pylint imports test_lib

flake8:
	flake8 zerorm test

pylint:
	pylint --rcfile=pylintrc zerorm -E

imports:
	isort -rc --check-only zerorm

imports_fix:
	isort -rc zerorm

test_lib:
	py.test --strict

