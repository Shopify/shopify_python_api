from ..base import ShopifyResource
from shopify import mixins
import shopify


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
        variant.attributes["product_id"] = self.id
        return variant.save()

    def save(self):
        start_api_version = "201910"
        api_version = ShopifyResource.version
        if api_version and (api_version.strip("-") >= start_api_version) and api_version != "unstable":
            if "variants" in self.attributes:
                for variant in self.variants:
                    if "inventory_quantity" in variant.attributes:
                        del variant.attributes["inventory_quantity"]
                    if "old_inventory_quantity" in variant.attributes:
                        del variant.attributes["old_inventory_quantity"]
        return super(ShopifyResource, self).save()
