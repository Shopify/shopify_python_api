import shopify
from ..base import ShopifyResource
from .payment import Payment
from .shipping_rate import ShippingRate

class Checkout(ShopifyResource):
    _primary_key = "token"
    extra_headers = {'X-Shopify-Checkout-Version': '2016-09-06'}

    def complete(self):
        self._load_attributes_from_response(self.post("complete"))

    def is_ready(self):
        if self.is_new():
            return false

        self.reload()
        status_code = int(shopify.ShopifyResource.connection.response.code)
        return status_code in [200, 201]

    def payments(self):
        return Payment.find(checkout_id=self.id)

    def shipping_rates(self):
        return ShippingRate.find(checkout_id=self.id)
