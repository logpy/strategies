from os.path import exists
from setuptools import setup

setup(name='strategies',
      version='0.1.1',
      description='Strategic Programming in python',
      url='http://github.com/logpy/strategies',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      license='BSD',
      packages=['strategies'],
      long_description=open('README.md').read() if exists("README.md") else "",
      zip_safe=False)
