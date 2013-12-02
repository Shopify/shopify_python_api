from ..base import ShopifyResource
import shopify.mixins as mixins

class Page(ShopifyResource, mixins.Metafields, mixins.Events):
    pass