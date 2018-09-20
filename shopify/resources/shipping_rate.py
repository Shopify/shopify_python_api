from ..base import ShopifyResource

class ShippingRate(ShopifyResource):
    _prefix_source = "/admin/checkouts/$checkout_id/"