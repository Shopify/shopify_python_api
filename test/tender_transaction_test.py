import shopify
from test.test_helper import TestCase


class TenderTransactionTest(TestCase):
    def setUp(self):
        super(TenderTransactionTest, self).setUp()
        self.fake("tender_transactions", method='GET', body=self.load_fixture('tender_transactions'))

    def test_should_load_all_tender_transactions(self):
        tender_transactions = shopify.TenderTransaction.find()
        self.assertEqual(3, len(tender_transactions))
        self.assertEqual([1, 2, 3], list(map(lambda t: t.id, tender_transactions)))
