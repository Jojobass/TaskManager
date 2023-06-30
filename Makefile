test:
	coverage run -m pytest
	COVERALLS_REPO_TOKEN=$(COVERALLS_REPO_TOKEN) coveralls

.PHONY: test