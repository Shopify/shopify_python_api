import shopify
from test.test_helper import TestCase


class ShippingZoneTest(TestCase):
    def test_get_shipping_zones(self):
        self.fake("shipping_zones", method='GET', body=self.load_fixture('shipping_zones'))
        shipping_zones = shopify.ShippingZone.find()
        self.assertEqual(1, len(shipping_zones))
        self.assertEqual(shipping_zones[0].name, "Some zone")
        self.assertEqual(3, len(shipping_zones[0].countries))
