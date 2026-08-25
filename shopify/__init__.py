import warnings

from shopify.version import VERSION
from shopify.session import Session, ValidationException
from shopify.resources import *
from shopify.limits import Limits
from shopify.api_version import *
from shopify.api_access import *
from shopify.collection import PaginatedIterator

warnings.warn(
    "ShopifyAPI is deprecated and no longer maintained. Use the 'shopifyapp' "
    "package instead: https://pypi.org/project/shopifyapp/",
    DeprecationWarning,
    stacklevel=2,
)
