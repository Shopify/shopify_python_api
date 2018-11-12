import shopify
from mock import patch
from test.test_helper import TestCase

class LimitsTest(TestCase):
    def setUp(self):
        super(LimitsTest, self).setUp()

        mock = patch('shopify.ShopifyResource.connection.response.get', side_effect=self.mock_limit_headers)
        mock.start()

        self.fake('shop')
        shopify.Shop.current()

    def tearDown(self):
        super(LimitsTest, self).tearDown()
        patch.stopall()

    def test_fetch_limits_total(self):
        self.assertEqual(40, shopify.Limits.credit_limit())

    def test_fetch_used_calls(self):
        self.assertEqual(1, shopify.Limits.credit_used())

    def test_calculate_remaining_calls(self):
        self.assertEqual(39, shopify.Limits.credit_left())

    def test_maxed_returns_true_when_credit_maxed_out(self):
        self.assertFalse(shopify.Limits.is_credit_maxed())

        with patch('shopify.ShopifyResource.connection.response.get', side_effect=self.mock_limit_headers_max) as mock:
            self.assertTrue(shopify.Limits.is_credit_maxed())

    def mock_limit_headers(self, key):
        if key == shopify.Limits.CREDIT_LIMIT_HEADER_PARAM:
            return '1/40'

    def mock_limit_headers_max(self, key):
        if key == shopify.Limits.CREDIT_LIMIT_HEADER_PARAM:
            return '40/40'
