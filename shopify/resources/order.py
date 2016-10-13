from ..base import ShopifyResource
from shopify import mixins
from .transaction import Transaction
from collections import Iterable


class Order(ShopifyResource, mixins.Metafields, mixins.Events):

    def close(self):
        self._load_attributes_from_response(self.post("close"))

    def open(self):
        self._load_attributes_from_response(self.post("open"))

    def cancel(self, **kwargs):
        self._load_attributes_from_response(self.post("cancel", **kwargs))

    def transactions(self):
        return Transaction.find(order_id=self.id)

    def capture(self, amount=""):
        return Transaction.create({"amount": amount, "kind": "capture", "order_id": self.id})

    def add_fulfillment(self, fulfillment):
        if not self.id:
            self.save()
        fulfillment.order_id = self.id

        result = fulfillment.save()
        if result:
            if not isinstance(self.attributes.get('fulfillments'), Iterable):
                self.fulfillments = []
            self.fulfillments.append(fulfillment)

        return result
