from ..base import ShopifyResource
import shopify.mixins as mixins

class CustomCollection(ShopifyResource, mixins.Metafields, mixins.Events):
    def products(self):
        return Product.find(collection_id=self.id)

    def add_product(self, product):
        return Collect.create(dict(collection_id=self.id, product_id=product.id))

    def remove_product(self, product):
        collect = Collect.find_first(collection_id=self.id, product_id=product.id)
        if collect:
            collect.destroy()