from ..base import ShopifyResource
import json


class Fulfillment(ShopifyResource):
    _prefix_source = "/orders/$order_id/"

    @classmethod
    def _prefix(cls, options={}):
        order_id = options.get("order_id")
        if order_id:
            return "%s/orders/%s" % (cls.site, order_id)
        else:
            return cls.site
    
    def cancel(self):
        self._load_attributes_from_response(self.post("cancel"))

    def complete(self):
        self._load_attributes_from_response(self.post("complete"))

    def open(self):
        self._load_attributes_from_response(self.post("open"))

    def update_tracking(self, tracking_info, notify_customer):
        fulfill = FulfillmentV2()
        fulfill.id = self.id
        self._load_attributes_from_response(fulfill.update_tracking(tracking_info, notify_customer))


class FulfillmentOrders(ShopifyResource):
    _prefix_source = "/orders/$order_id/"


class FulfillmentV2(ShopifyResource):
    _singular = "fulfillment"
    _plural = "fulfillments"

    def update_tracking(self, tracking_info, notify_customer):
        body = {"fulfillment": {"tracking_info": tracking_info, "notify_customer": notify_customer}}
        return self.post("update_tracking", json.dumps(body).encode())
