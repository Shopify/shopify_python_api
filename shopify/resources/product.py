from ..base import ShopifyResource
from shopify import mixins
import shopify
from collections import Iterable


class Product(ShopifyResource, mixins.Metafields, mixins.Events):

    def price_range(self):
        prices = [float(variant.price) for variant in self.variants]
        f = "%0.2f"
        min_price = min(prices)
        max_price = max(prices)
        if min_price != max_price:
            return "%s - %s" % (f % min_price, f % max_price)
        else:
            return f % min_price

    def collections(self):
        return shopify.CustomCollection.find(product_id=self.id)

    def smart_collections(self):
        return shopify.SmartCollection.find(product_id=self.id)

    def add_to_collection(self, collection):
        return collection.add_product(self)

    def remove_from_collection(self, collection):
        return collection.remove_product(self)

    def add_variant(self, variant):
        if not self.id:
            self.save()
        variant.attributes['product_id'] = self.id

        result =  variant.save()
        if result:
            if not isinstance(self.attributes.get('variants'), Iterable):
                self.variants = []
            self.variants.append(variant)

        return result

    def add_image(self, image):
        if not self.id:
            self.save()
        image.attributes['product_id'] = self.id

        result = image.save()
        if result:
            if not isinstance(self.attributes.get('images'), Iterable):
                self.images = []
            self.images.append(image)

        return result
