import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        _test_args = [
            '--ignore=setup.py',
            '--verbose',
            '--durations=5',
            '--doctest-modules',
        ]
        extra_args = os.environ.get('PYTEST_EXTRA_ARGS')
        if extra_args is not None:
            _test_args.extend(extra_args.split())
        self.test_args = _test_args
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(name='strategies',
      version='0.2.3',
      description='Strategic Programming in python',
      url='http://github.com/logpy/strategies',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      install_requires=open('dependencies.txt').read().split('\n'),
      tests_require=['pytest'],
      cmdclass = {'test': PyTest},
      license='BSD',
      packages=['strategies', 'strategies.branch'],
      long_description=open('README.md').read() if os.path.exists("README.md") else "",
      zip_safe=False)
