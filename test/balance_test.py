import shopify
from test.test_helper import TestCase


class BalanceTest(TestCase):
    prefix = "/admin/api/unstable/shopify_payments"

    def test_get_balance(self):
        self.fake("balance", method="GET", prefix=self.prefix, body=self.load_fixture("balance"))
        balance = shopify.Balance.find()
        self.assertGreater(len(balance), 0)
