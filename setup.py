#!/usr/bin/env python

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = ['pymysql', 'requests']

setup(name='liked-deposit-eos',
      version='0.0.1',
      description='this project work for like-D eos deposit',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
      ],
      url='',
      keywords='eos, block chain, transfer, deposit',
      packages=find_packages(),
      zip_safe=False,
      install_requires=requires,
      test_suite=""
      )
