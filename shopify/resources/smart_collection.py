from ..base import ShopifyResource
from shopify import mixins

class SmartCollection(ShopifyResource, mixins.Metafields, mixins.Events):

    def products(self):
        return Product.find(collection_id=self.id)
