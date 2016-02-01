test:
	@echo "---> running tests"
	@cd tests; py.test . --tb=short -v
