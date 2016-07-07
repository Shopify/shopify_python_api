import shopify
from test.test_helper import TestCase

class RefundTest(TestCase):
    def setUp(self):
        super(RefundTest, self).setUp()
        self.fake("orders/450789469/refunds/509562969", method='GET', body=self.load_fixture('refund'))

    def test_should_find_a_specific_refund(self):
        refund = shopify.Refund.find(509562969, order_id=450789469)
        self.assertEqual("209.00", refund.transactions[0].amount)
