from ..base import ShopifyResource
import shopify.mixins as mixins

class SmartCollection(ShopifyResource, mixins.Metafields, mixins.Events):
    def products(self):
        return Product.find(collection_id=self.id)
