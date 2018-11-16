all: bin

bin: setup.py versions.cfg
	-rm -r bin
	buildout

.PHONY: clean
clean:
	-rm bin/*

.PHONY: format
format:
	autopep8 -ria --max-line-length 120 app
