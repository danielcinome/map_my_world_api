dev:
	python runner.py
test:
	python -m pytest -svv app/tests --disable-warnings
test-routers:
	python -m pytest -svv app/tests/routers --disable-warnings
test-modules:
	python -m pytest -svv app/tests/modules --disable-warnings