PYTHON=python3
PYTHONPATH=./
name=shhh
version=$(shell PYTHONPATH=$(PYTHONPATH) $(PYTHON) -c "import $(name); print($(name).__version__)")
PY_TESTS=test/test_*.py

all:
	@echo "make dist to 1) push and tag to github, and 2) upload to pypi."

# for running from IDEs (e.g., TextMate)
.PHONY: run
run: test

.PHONY: version
version:
	@echo $(version)

.PHONY: dist
dist: clean typecheck # test
	git tag $(name)-$(version)
	git push
	git push --tags origin
	$(PYTHON) setup.py sdist
	$(PYTHON) -m twine upload dist/*

.PHONY: lint
lint:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pylint --rcfile=test/pylintrc $(name)

.PHONY: test
test: $(PY_TESTS)

.PHONY: $(PY_TESTS)
$(PY_TESTS):
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) $@

.PHONY: typecheck
typecheck:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m mypy --config-file=test/mypy.ini $(name)

.PHONY: clean
clean:
	rm -rf build dist MANIFEST $(name).egg-info
	find . -type f -name \*.pyc -exec rm {} \;
	find . -d -type d -name __pycache__ -exec rm -rf {} \;
