import shopify
from test.test_helper import TestCase


class RefundTest(TestCase):
    def setUp(self):
        super(RefundTest, self).setUp()
        self.fake("orders/450789469/refunds/509562969", method='GET', body=self.load_fixture('refund'))

    def test_should_find_a_specific_refund(self):
        refund = shopify.Refund.find(509562969, order_id=450789469)
        self.assertEqual("209.00", refund.transactions[0].amount)

    def test_calculate_refund_for_order(self):
        self.fake(
            "orders/450789469/refunds/calculate",
            method="POST",
            code=201,
            body=self.load_fixture('refund_calculate'),
            headers={'Content-type': 'application/json'},
        )
        refund = shopify.Refund.calculate(
            order_id=450789469,
            refund_line_items=[{'line_item_id': 518995019, 'quantity': 1}]
        )

        self.assertEqual("suggested_refund", refund.transactions[0].kind)
        self.assertEqual("41.94", refund.transactions[0].amount)
        self.assertEqual(518995019, refund.refund_line_items[0].line_item_id)
