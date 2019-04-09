from ..base import ShopifyResource


class Fulfillment(ShopifyResource):
    _prefix_source = "/orders/$order_id/"

    def cancel(self):
        self._load_attributes_from_response(self.post("cancel"))

    def complete(self):
        self._load_attributes_from_response(self.post("complete"))

    def open(self):
        self._load_attributes_from_response(self.post("open"))
