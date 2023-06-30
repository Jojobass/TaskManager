test:
	coverage run -m pytest
	coverage json
	COVERALLS_REPO_TOKEN=$(COVERALLS_REPO_TOKEN) coveralls

.PHONY: test