#!/usr/bin/env python

import skritter


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


packages = [
    'skritter',
    ]


requires = []


setup(
    name='skritter',
    version=skritter.__version__,
    author='Geoff van der Meer',
    author_email='gmwils@gmail.com',
    packages=packages,
    install_requires=requires,
    )
