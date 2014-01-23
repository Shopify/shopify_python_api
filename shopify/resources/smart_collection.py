from ..base import ShopifyResource
from shopify import mixins
import product


class SmartCollection(ShopifyResource, mixins.Metafields, mixins.Events):

    def products(self):
        return product.Product.find(collection_id=self.id)
