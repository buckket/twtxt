# always rebuild docs
# -> needed because of directory named docs/
.PHONY: docs

all: test docs

test:
	@echo "---> running tests using tox"
	@python3 -m tox

pytest:
	@echo "---> running tests directly"
	@py.test --tb=short -v --cov twtxt/ tests/

coverage:
	@echo "---> building coverage report"
	@coverage html

docs:
	@echo "---> generating sphinx documentation"
	@cd docs; make html

publish:
	@echo "---> uploading to PyPI"
	@python3 setup.py register
	@python3 setup.py sdist upload
	@rm -fr dist .egg
