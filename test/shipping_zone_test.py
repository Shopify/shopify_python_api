import shopify
from test.test_helper import TestCase

class ShippingZoneTest(TestCase):
    def test_check_shipping_zone_url(self):
        s = shopify.ShippingZone()
        self.assertEqual(s._collection_path(),"admin/shipping_zones.json")
