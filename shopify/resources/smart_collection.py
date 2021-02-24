from ..base import ShopifyResource
from shopify import mixins
import shopify


class SmartCollection(ShopifyResource, mixins.Metafields, mixins.Events):
    def products(self):
        return shopify.Product.find(collection_id=self.id)
