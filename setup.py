#/usr/bin/env python
from setuptools import setup

try:
    readme = open("README.md")
    long_description = str(readme.read())
finally:
    readme.close()

setup(
    name='pyziptax',
    version='1.0',
    description='Python API for accessing sales tax information from Zip-Tax.com',
    long_description=long_description,
    author='Albert Wang',
    author_email='aywang31@gmail.com',
    url='http://github.com/albertyw/pyziptax',
    packages=['pyziptax', ],
    install_requires=[
        'requests>=1.1.0',
    ],
    license='Apache',
    test_suite="tests",
)
