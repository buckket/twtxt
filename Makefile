test:
	@echo "---> running tests using tox"
	@python3 -m tox

publish:
	@echo "---> uploading to PyPI"
	@python3 setup.py register
	@python3 setup.py sdist upload
	@rm -fr dist .egg
