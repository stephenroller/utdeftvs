#!/usr/bin/env python

import os
import os.path
from setuptools import setup

setup(name='utdeftvs',
      version='0.1',
      description='Tools for building and using distributional vector spaces.',
      author='Stephen Roller',
      author_email='roller@cs.utexas.edu',
      license='MIT',
      packages=['utdeftvs'],
      zip_safe=False,
      scripts=[os.path.join("bin", x) for x in os.listdir("bin")],
      )

