import shopify
from test.test_helper import TestCase


class TransactionsTest(TestCase):
    prefix = '/admin/api/unstable/shopify_payments/balance'

    def test_get_payouts_transactions(self):
        self.fake('transactions', method='GET', prefix=self.prefix,
                  body=self.load_fixture('payouts_transactions'))
        transactions = shopify.Transactions.find()
        self.assertGreater(len(transactions), 0)
