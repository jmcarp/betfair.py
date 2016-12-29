# -*- coding: utf-8 -*-

import os
import re
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


INSTALL_REQUIRES = [
    'six>=1.9.0',
    'enum34>=1.0.4',
    'invoke>=0.10.1',
    'requests>=2.6.2',
    'decorator>=3.4.2',
    'inflection>=0.3.0',
    'schematics>=1.0.4,<2.0.0',
    'python-dateutil>=2.4.2',
]
TEST_REQUIRES = [
    'pytest',
    'responses',
]


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--verbose']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name='betfair.py',
    version=find_version('betfair/__init__.py'),
    description='Python client for the Betfair API '
                '(https://api.developer.betfair.com/)',
    long_description=open('README.rst').read(),
    author='Joshua Carp',
    author_email='jm.carp@gmail.com',
    url='https://github.com/jmcarp/betfair.py',
    packages=find_packages(exclude=('test*', )),
    package_dir={'betfair': 'betfair'},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='tests',
    tests_require=TEST_REQUIRES,
    cmdclass={'test': PyTest}
)
