import json

from ..base import ShopifyResource


class Fulfillment(ShopifyResource):
    _prefix_sources = {
        ("order_id",): "/orders/$order_id/",
        ("fulfillment_order_id",): "/fulfillment_orders/$fulfillment_order_id/",
    }
    # cla
    @classmethod
    def _split_options(cls, options):
        if cls._prefix_sources and options:
            options_tuples = tuple(options)
            if options_tuples in cls._prefix_sources:
                cls._prefix_source = cls._prefix_sources[options_tuples]

        return super()._split_options(options)

    def cancel(self):
        self._load_attributes_from_response(self.post("cancel"))

    def complete(self):
        self._load_attributes_from_response(self.post("complete"))

    def open(self):
        self._load_attributes_from_response(self.post("open"))

    def update_tracking(self, tracking_info, notify_customer):
        body = {"fulfillment": {"tracking_info": tracking_info, "notify_customer": notify_customer}}
        return self.post("update_tracking", json.dumps(body).encode())


class FulfillmentOrders(ShopifyResource):
    _prefix_sources = {
        ("order_id",): "/orders/$order_id/",
    }

    @classmethod
    def _split_options(cls, options):
        if cls._prefix_sources and options:
            options_tuples = tuple(options)
            if options_tuples in cls._prefix_sources:
                cls._prefix_source = cls._prefix_sources[tuple(options)]

        return super()._split_options(options)
