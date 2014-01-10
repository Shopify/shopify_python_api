import shopify
from test_helper import TestCase

class TransactionTest(TestCase):
    def setUp(self):
        super(TransactionTest, self).setUp()
        self.fake("orders/450789469/transactions/389404469", method='GET', body=self.load_fixture('transaction'))

    def test_should_find_a_specific_transaction(self):
        transaction = shopify.Transaction.find(389404469, order_id=450789469)
        self.assertEqual("409.94", transaction.amount)
