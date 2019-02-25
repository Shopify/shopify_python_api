# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

RELEASE_LEVELS = [ALPHA, BETA, RELEASE_CANDIDATE, FINAL] = [
    'alpha', 'beta', 'candidate', 'final'
]
RELEASE_LEVELS_DISPLAY = {ALPHA: ALPHA,
                          BETA: BETA,
                          RELEASE_CANDIDATE: 'rc',
                          FINAL: ''}

# version_info format: (MAJOR, MINOR, MICRO, RELEASE_LEVEL, SERIAL)
# inspired by Python's own sys.version_info, in order to be
# properly comparable using normal operarors, for example:
#  (6,1,0,'beta',0) < (6,1,0,'candidate',1) < (6,1,0,'candidate',2)
#  (6,1,0,'candidate',2) < (6,1,0,'final',0) < (6,1,2,'final',0)
version_info = (4, 0, 0, BETA, 2, '')

version = '.'.join(str(s) for s in version_info[:3]) + RELEASE_LEVELS_DISPLAY[
    version_info[3]] + str(version_info[4] or '') + version_info[5]

series = serie = major_version = '.'.join(str(s) for s in version_info[:3])

product_name = 'ShopifyAPI'
description = 'Shopify API for Python'
long_description = '''The ShopifyAPI library allows python developers to
programmatically access the admin section of stores using an ActiveResource
like interface similar the ruby Shopify API gem. The library makes HTTP
requests to Shopify in order to list, create, update, or delete
resources (e.g. Order, Product, Collection).
'''
classifiers = """Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Software Development
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
"""
url = 'https://github.com/Shopify/shopify_python_api'
author = 'Shopify'
author_email = 'developers@shopify.com'
license = 'MIT License'
