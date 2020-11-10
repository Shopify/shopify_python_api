from ..base import ShopifyResource
from shopify import mixins


class Disputes(ShopifyResource, mixins.Metafields):
    _prefix_source = "/shopify_payments/"
