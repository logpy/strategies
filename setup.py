from os.path import exists
from setuptools import setup

setup(name='strategies',
      version='0.2.0',
      description='Strategic Programming in python',
      url='http://github.com/logpy/strategies',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      install_requires=open('dependencies.txt').read().split('\n'),
      license='BSD',
      packages=['strategies', 'strategies.branch'],
      long_description=open('README.md').read() if exists("README.md") else "",
      zip_safe=False)
