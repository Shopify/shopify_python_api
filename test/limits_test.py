import shopify
from mock import patch
from test.test_helper import TestCase


class LimitsTest(TestCase):
    """
    API Calls Limit Tests

    Conversion of test/limits_test.rb
    """

    @classmethod
    def setUpClass(self):
        self.original_headers = None

    def setUp(self):
        super(LimitsTest, self).setUp()
        self.fake('shop')
        shopify.Shop.current()
        # TODO: Fake not support Headers
        self.original_headers = shopify.Shop.connection.response.headers

    def tearDown(self):
        super(LimitsTest, self).tearDown()
        shopify.Shop.connection.response.headers = self.original_headers

    def test_raise_error_no_header(self):
        with self.assertRaises(Exception):
            shopify.Limits.credit_left()

    def test_raise_error_invalid_header(self):
        with patch.dict(shopify.Shop.connection.response.headers, {'bad': 'value'}, clear=True):
            with self.assertRaises(Exception):
                shopify.Limits.credit_left()

    def test_fetch_limits_total(self):
        with patch.dict(
            shopify.Shop.connection.response.headers, {'X-Shopify-Shop-Api-Call-Limit': '40/40'}, clear=True
        ):
            self.assertEqual(40, shopify.Limits.credit_limit())

    def test_fetch_used_calls(self):
        with patch.dict(
            shopify.Shop.connection.response.headers, {'X-Shopify-Shop-Api-Call-Limit': '1/40'}, clear=True
        ):
            self.assertEqual(1, shopify.Limits.credit_used())

    def test_calculate_remaining_calls(self):
        with patch.dict(
            shopify.Shop.connection.response.headers, {'X-Shopify-Shop-Api-Call-Limit': '292/300'}, clear=True
        ):
            self.assertEqual(8, shopify.Limits.credit_left())

    def test_maxed_credits_false(self):
        with patch.dict(
            shopify.Shop.connection.response.headers, {'X-Shopify-Shop-Api-Call-Limit': '125/300'}, clear=True
        ):
            self.assertFalse(shopify.Limits.credit_maxed())

    def test_maxed_credits_true(self):
        with patch.dict(
            shopify.Shop.connection.response.headers, {'X-Shopify-Shop-Api-Call-Limit': '40/40'}, clear=True
        ):
            self.assertTrue(shopify.Limits.credit_maxed())
