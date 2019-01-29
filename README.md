# amazing

Web project template of Python3 using tornado and built with buildout.

# Dependence

Python 3.5+

# Installation

1. Install buildout via `pip install zc.buildout` on Linux(append `--user` or `sudo`);
2. run `buildout`;

PS: On MacOS, run `brew install openssl@1.1` first;

# Start Service

Run `bin/amazing_api` using default port 8000 or `bin/amazing_api --port=8xxx`.

Run `curl http://localhost:8xxx` will get a message in json format:

```json
{
    "msg": "hello"
}
```