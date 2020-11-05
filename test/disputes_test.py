import shopify
from test.test_helper import TestCase


class DisputeTest(TestCase):
    prefix = '/admin/api/unstable/shopify_payments'

    def test_get_dispute(self):
        self.fake('disputes', method='GET', prefix=self.prefix, body=self.load_fixture('disputes'))
        disputes = shopify.Disputes.find()
        self.assertGreater(len(disputes), 0)

    def test_get_one_dispute(self):
        self.fake('disputes/1052608616', method='GET',
                  prefix=self.prefix, body=self.load_fixture('disputes'))
        disputes = shopify.Disputes.find(1052608616)
        self.assertEqual('won', disputes.status)
