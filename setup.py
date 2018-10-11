# coding=utf-8
from os import path
from setuptools import find_packages, setup

from app import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().split('\n')

setup(
    name='amazing',
    version=__version__,
    license='PRIVATE',
    author='',
    author_email='',
    description='amazing pay',
    url='git@github.com:astroshot/amazing.git',
    packages=find_packages(exclude=['static']),
    zip_safe=False,
    install_requires=[line.strip() for line in requirements if line],
    entry_points={
        'console_scripts': [
            'amazing_api = app.main:main',
        ]
    }
)
