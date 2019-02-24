#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from os.path import join, dirname

# Load release variables
exec(open(join(dirname(__file__), 'shopify', 'release.py'), 'rb').read())
lib_name = 'shopify'

setup(
    name=product_name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    packages=find_packages(),
    package_dir={'%s' % lib_name: 'shopify'},
    scripts=['scripts/shopify_api.py'],
    license=license,
    include_package_data=True,
    install_requires=[
        'pyactiveresource>=2.1.2',
        'PyYAML',
        'six',
        'pyopenssl',
    ],
    extras_require={
        'SSL': ['pyopenssl'],
    },
    test_suite='test',
    tests_require=[
        'mock>=1.0.1',
        'pytest'
    ],
    platforms='Any',
    classifiers=[c for c in classifiers.split('\n') if c],
)
