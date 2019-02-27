#!/usr/bin/env bash
sed 1d versions.cfg | egrep -v '(^#.*|setuptools|zc\.*|.*\.recipe\..*)' | sed -e 's/ *= */==/g' | sed -e '/^$/d' | xargs pip install