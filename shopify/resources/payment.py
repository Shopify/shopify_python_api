from ..base import ShopifyResource

class Payment(ShopifyResource):
    _prefix_source = "/admin/checkouts/$checkout_id/"