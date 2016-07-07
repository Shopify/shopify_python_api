from ..base import ShopifyResource


class Refund(ShopifyResource):
    _prefix_source = "/admin/orders/$order_id/"
