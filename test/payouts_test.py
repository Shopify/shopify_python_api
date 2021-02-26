import shopify
from test.test_helper import TestCase


class PayoutsTest(TestCase):
    prefix = '/admin/api/unstable/shopify_payments'

    def test_get_payouts(self):
        self.fake('payouts', method='GET', prefix=self.prefix, body=self.load_fixture('payouts'))
        payouts = shopify.Payouts.find()
        self.assertGreater(len(payouts), 0)

    def test_get_one_payout(self):
        self.fake('payouts/623721858', method='GET', prefix=self.prefix, body=self.load_fixture('payout'))
        payouts = shopify.Payouts.find(623721858)
        self.assertEqual('paid', payouts.status)
        self.assertEqual('41.90', payouts.amount)
