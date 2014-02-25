from ..base import ShopifyResource
from shopify import mixins


class Page(ShopifyResource, mixins.Metafields, mixins.Events):
    pass
