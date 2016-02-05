test:
	@echo "---> running tests"
	@py.test --tb=short -v --cov twtxt/ tests/
