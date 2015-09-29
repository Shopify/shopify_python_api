from ..base import ShopifyResource


class Discount(ShopifyResource):

    def disable(self):
        self._load_attributes_from_response(self.post("disable"))

    def enable(self):
        self._load_attributes_from_response(self.post("enable"))
