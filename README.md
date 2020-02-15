# amazing

A web project template of Python3 using tornado and built with buildout.

## Dependence

1. Python 3 (I'm using Python 3.7.2, and I suppose Python 3.5+ will do)
2. MySQL (On MacOS, I'm using mysql@5.7, while on Linux, I'm using mariadb)

## Installation

### Linux

1. `sudo python -m pip install zc.buildout` (or `python -m pip install zc.buildout --user`);
2. Run `make all` (or reading Makefile);

### MacOS

1. On MacOS, run `brew install openssl@1.1`, and add this to your bashrc or zshrc;
```bash
# mysql 5.7 at MacOS
export MYSQL_HOME="/usr/local/opt/mysql@5.7"
export PATH="$MYSQL_HOME/bin:$PATH"
export PKG_CONFIG_PATH="$MYSQL_HOME/lib/pkgconfig"

# For compilers to find mysql@5.7
export LDFLAGS="-L/usr/local/opt/mysql@5.7/lib -L/usr/local/opt/openssl@1.1/lib"
export CPPFLAGS="-I/usr/local/opt/mysql@5.7/include -I/usr/local/opt/openssl@1.1/include"
```

2. `python -m pip install zc.buildout`;
3. Run `make all`;

### Export pip packages

```bash
pip freeze | grep -Eo '(.*==)' | sed 's/==//g' > requirements.txt
```

## Start Service

Run `bin/amazing_api` using default port 8000 and env dev or `bin/amazing_api --port=8xxx --env=dev|prod`.

Run `curl http://localhost:8xxx` will get a message in json format:

```json
{
    "msg": "hello"
}
```

## Use virtualenv and virtualenvwrapper

`virtualenv` is a tool to create isolated Python environments. It creates an environment that has its own installation 
directories, that doesn’t share libraries with other virtualenv environments (and optionally doesn’t access the globally
 installed libraries either). Docs can be found [here](https://virtualenv.pypa.io/en/latest/). 

`virtualenvwrapper` is a set of extensions to Ian Bicking’s virtualenv tool. The extensions include wrappers for 
creating and deleting virtual environments and otherwise managing your development workflow, making it easier to work 
on more than one project at a time without introducing conflicts in their dependencies. 
Docs can be found [here](https://virtualenvwrapper.readthedocs.io/en/latest/).

#### Installation

1. Run `python -m pip install virtualenv virtualenvwrapper`;
2. Add `source /usr/local/bin/virtualenvwrapper.sh` to your bashrc or zshrc (or `source /usr/bin/virtualenvwrapper.sh`, 
you should locate on your own OS using `which virtualenvwrapper.sh`);

#### Usage

| Command | Description |
|---|---|
| `mkvirtualenv` | create a virtual env using specified python, default using `env python` |
| `lsvirtualenv` | list all virtual env created |
| `rmvirtualenv` | remove specified virtual env on disk |
| `workon` | list all virtualenv if no env is specified or activate specified env |
