import shopify
from test.test_helper import TestCase

class ShippingRateTest(TestCase):
    def test_find_all_shipping_rates_for_checkout(self):
        self.fake('checkouts', method='GET', status=200, body=self.load_fixture('checkouts'))
        checkouts = shopify.Checkout.find()

        self.fake(
            "checkouts/%s/shipping_rates" % checkouts[0].id,
            method='GET',
            status=200,
            body=self.load_fixture('shipping_rates')
        )
        shipping_rates = shopify.ShippingRate.find(checkout_id=checkouts[0].id)

        self.assertEqual(2, len(shipping_rates))
        self.assertEqual("canada_post-INT.TP.BOGUS-4.00", shipping_rates[0].id)
