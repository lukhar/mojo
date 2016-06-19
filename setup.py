#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='mojo',
      packages=find_packages(),
      install_requires=['watchdog', 'click', 'future'],
      license='MIT',
      version='0.1.3',
      description='Continous Test Runner',
      author='Lukasz Haratym',
      author_email='lukasz.har@gmail.com',
      url='https://github.com/lukhar/mojo',
      entry_points={'console_scripts': ['mojo = mojo:main']}
      )
