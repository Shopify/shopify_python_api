from ..base import ShopifyResource


class FulfillmentEvent(ShopifyResource):
    _prefix_source = "/orders/$order_id/fulfillments/$fulfillment_id/"
    _singular = "event"
    _plural = "events"

    @classmethod
    def _prefix(cls, options={}):
        order_id = options.get("order_id")
        fulfillment_id = options.get("fulfillment_id")
        event_id = options.get("event_id")

        return "%s/orders/%s/fulfillments/%s" % (cls.site, order_id, fulfillment_id)

    def save(self):
        status = self.attributes["status"]
        if status not in [
            "label_printed",
            "label_purchased",
            "attempted_delivery",
            "ready_for_pickup",
            "picked_up",
            "confirmed",
            "in_transit",
            "out_for_delivery",
            "delivered",
            "failure",
        ]:
            raise AttributeError("Invalid status")
        return super(ShopifyResource, self).save()
