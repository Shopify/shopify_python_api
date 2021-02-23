from ..base import ShopifyResource
from shopify import mixins
from .transaction import Transaction


class Order(ShopifyResource, mixins.Metafields, mixins.Events):
    _prefix_source = "/customers/$customer_id/"

    @classmethod
    def _prefix(cls, options={}):
        customer_id = options.get("customer_id")
        if customer_id:
            return "%s/customers/%s" % (cls.site, customer_id)
        else:
            return cls.site

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
