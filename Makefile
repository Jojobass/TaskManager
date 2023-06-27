test:
	coverage run -m pytest
	COVERALLS_REPO_TOKEN=gKhOR25eN5C221BQAY4mNUs81zZ0DQqA4 coveralls

.PHONY: test