import shopify
import json
from test.test_helper import TestCase

class AbandonedCheckoutTest(TestCase):
    def setUp(self):
        super(AbandonedCheckoutTest, self).setUp()
        self.expected_checkouts = json.loads(self.load_fixture('abandoned_checkouts'))['checkouts']
        self.expected_checkout_id = json.loads(self.load_fixture('abandoned_checkout'))['checkout']['id']

    def test_all_should_return_all_abandoned_checkouts(self):
        self.fake('checkouts', method='GET', code=200, body=self.load_fixture('abandoned_checkouts'))

        checkouts = shopify.AbandonedCheckout.find()
        self.assertEqual(self.expected_checkout_id, checkouts[0].id)
        self.assertEqual(len(self.expected_checkouts), len(checkouts))
