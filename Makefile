.PHONY: clean build test format

clean:
	-rm bin/* nosetests.xml coverage.xml .coverage

build:
	buildout -c buildout.cfg
	echo 'buildout finished...'

test:
	bin/test tests

format:
	autopep8 -ria --max-line-length 120 src script

rebuild: clean build
	echo 'rebuild finished...'
