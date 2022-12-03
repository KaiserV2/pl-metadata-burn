from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'metadata_burn',
    version          = '0.1',
    description      = 'An app to add metadata to a PNG image',
    long_description = readme,
    author           = 'John Pastore',
    author_email     = 'dev@babyMRI.org',
    url              = 'http://wiki',
    packages         = ['metadata_burn'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'metadata_burn = metadata_burn.__main__:main'
            ]
        }
)
