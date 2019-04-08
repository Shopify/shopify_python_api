from ..base import ShopifyResource


class Transaction(ShopifyResource):
    _prefix_source = "/orders/$order_id/"
