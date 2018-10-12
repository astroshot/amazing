bin: setup.py versions.cfg
    -rm -r bin
    buildout

.PHONY: clean
clean:
    -rm -r bin
