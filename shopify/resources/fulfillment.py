from ..base import ShopifyResource


class Fulfillment(ShopifyResource):
    _prefix_source = "/orders/$order_id/"

    def cancel(self):
        self._load_attributes_from_response(self.post("cancel"))

    def complete(self):
        self._load_attributes_from_response(self.post("complete"))

    def open(self):
        self._load_attributes_from_response(self.post("open"))


class FulfillmentOrders(ShopifyResource):
    @classmethod
    def find(cls, id_=None, from_=None, **kwargs):
        if id_:
            cls._prefix_source = ''
        else:
            cls._prefix_source = "/orders/$order_id/"
        resource = super(FulfillmentOrders, cls).find(id_=id_, from_=from_, **kwargs)
        return resource
