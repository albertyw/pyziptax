#/usr/bin/env python
from setuptools import setup

try:
    readme = open("README.rst")
    long_description = str(readme.read())
finally:
    readme.close()

setup(
    name='pyziptax',
    version='1.1',
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
    tests_require=[
        'mock>=1.0.1',
        'tox',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Localization',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
)
