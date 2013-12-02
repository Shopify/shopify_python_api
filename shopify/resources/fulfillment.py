from ..base import ShopifyResource

class Fulfillment(ShopifyResource):
    _prefix_source = "/admin/orders/$order_id/"