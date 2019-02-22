#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from os.path import join, dirname

# Load release variables
exec(open(join(dirname(__file__), 'shopify', 'release.py'), 'rb').read())
lib_name = 'shopify'

with open("requirements.txt", encoding="utf-8") as f:
    install_requires = f.read().splitlines()

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
    install_requires=install_requires,
    python_requires='>=3.5',
    extras_require={
        'SSL': ['pyopenssl'],
    },
    test_suite='test',
    tests_require=[
        'mock',
    ],
    platforms='Any',
    classifiers=[c for c in classifiers.split('\n') if c],
)
