# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

# Python 2.7 will reach the end of life in January 2020
# Python 3.4 will reach the end of life in March 2019
# import sys
# assert sys.version_info >= (3, 5), "ShopifyAPI requires Python >= 3.5 to run"

from shopify import release  # noqa: E402
from shopify.session import Session, ValidationException  # noqa: E402,F401
from shopify.resources import *  # noqa: E402,F401,F403
from shopify.limits import Limits  # noqa: E402,F401

__version__ = release.version
__author__ = release.author
