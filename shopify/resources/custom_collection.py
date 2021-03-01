from ..base import ShopifyResource
from shopify import mixins
import shopify


class CustomCollection(ShopifyResource, mixins.Metafields, mixins.Events):
    def products(self):
        return shopify.Product.find(collection_id=self.id)

    def add_product(self, product):
        return shopify.Collect.create({"collection_id": self.id, "product_id": product.id})

    def remove_product(self, product):
        collect = shopify.Collect.find_first(collection_id=self.id, product_id=product.id)
        if collect:
            collect.destroy()
