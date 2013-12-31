init:
	pip install -r requirements.txt

check:
	py.test test

coverage:
	py.test --verbose --cov-report term-missing --cov=skritter test
