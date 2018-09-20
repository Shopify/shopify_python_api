import shopify
import json
from test.test_helper import TestCase

class PaymentTest(TestCase):
    def setUp(self):
        super(PaymentTest, self).setUp()
        self.checkout_id = json.loads(self.load_fixture('checkout'))['checkout']['token']
        self.expected_payment = json.loads(self.load_fixture('payment'))['payment']

    def test_create_a_new_payment(self):
        self.fake(
            "checkouts/%s/payments" % self.checkout_id,
            method='POST',
            status=200,
            body=self.load_fixture('payment'),
            headers={'Content-type': 'application/json'}
        )
        payment = shopify.Payment.create({'checkout_id': self.checkout_id})

        self.assertEqual(self.expected_payment['unique_token'], payment.unique_token)