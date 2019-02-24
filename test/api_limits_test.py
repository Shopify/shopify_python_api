import shopify
from mock import patch
from test.test_helper import TestCase


class ApiLimitsTest(TestCase):

    @classmethod
    def setUpClass(self):
        self.original_headers = None

    def setUp(self):
        super(ApiLimitsTest, self).setUp()
        self.fake('shop')
        shopify.Shop.current()
        # TODO: Fake not support Headers
        #       Force it with mock or can copy and edit fake() on test_helper
        self.original_headers = shopify.Shop.connection.response.headers

    def tearDown(self):
        super(ApiLimitsTest, self).tearDown()
        shopify.Shop.connection.response.headers = self.original_headers

    def test_api_limits_error(self):
        with self.assertRaises(ValueError):
            shopify.ApiLimits.status()

    def test_api_limits_invalid(self):
        # TODO: Fake not support Headers, force this value
        with patch.dict(
                    shopify.Shop.connection.response.headers,
                    {'X-Shopify-Shop-Api-Call-Limit': '0/0'},
                    clear=True):
            self.assertNotEqual("1/40", shopify.ApiLimits.status())

    def test_api_limits_valid(self):
        # TODO: Fake not support Headers, force this value
        with patch.dict(
                    shopify.Shop.connection.response.headers,
                    {'X-Shopify-Shop-Api-Call-Limit': '1/40'},
                    clear=True):
            self.assertEqual("1/40", shopify.ApiLimits.status())

    def test_api_limits_left(self):
        # TODO: Fake not support Headers, force this value
        with patch.dict(
                    shopify.Shop.connection.response.headers,
                    {'X-Shopify-Shop-Api-Call-Limit': '32/40'},
                    clear=True):
            self.assertEqual(8, shopify.ApiLimits.left())

    def test_api_limits_end(self):
        # TODO: Fake not support Headers, force this value
        with patch.dict(
                    shopify.Shop.connection.response.headers,
                    {'X-Shopify-Shop-Api-Call-Limit': '40/40'},
                    clear=True):
            self.assertEqual(0, shopify.ApiLimits.left())
