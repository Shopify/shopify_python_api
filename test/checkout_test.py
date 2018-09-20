import shopify
import json
from test.test_helper import TestCase

class CheckoutTest(TestCase):

    def setUp(self):
        super(CheckoutTest, self).setUp()
        self.expected_checkouts = json.loads(self.load_fixture('checkouts'))['checkouts']
        self.expected_checkout_id = json.loads(self.load_fixture('checkout'))['checkout']['token']

    def find_expected_checkout(self, code=200):
        self.fake(
            "checkouts/%s" % self.expected_checkout_id,
            method='GET',
            code=code,
            body=self.load_fixture('checkout')
        )
        checkout = shopify.Checkout.find(self.expected_checkout_id)

        return checkout

    def test_create_a_checkout(self):
        self.fake(
            'checkouts',
            method='POST',
            code=201,
            body=self.load_fixture('checkout'),
            headers={'Content-type': 'application/json'}
        )

        checkout = shopify.Checkout.create({'email': 'test@mailinator.com'})

        self.assertEqual(self.expected_checkout_id, checkout.id)

    def test_get_all_checkouts_indexed_by_token(self):
        self.fake('checkouts', method='GET', body=self.load_fixture('checkouts'))

        checkouts = shopify.Checkout.find()

        self.assertEqual(self.expected_checkout_id, checkouts[0].id)
        self.assertEqual(len(self.expected_checkouts), len(checkouts))

    def test_complete_a_checkout(self):
        checkout = self.find_expected_checkout()

        self.fake(
            "checkouts/%s/complete" % self.expected_checkout_id,
            method='POST',
            code=200,
            body=self.load_fixture('checkout'),
            headers={'Content-type': 'application/json', 'Content-length': '0'}
        )
        checkout.complete()

    def test_is_ready_returns_true_when_status_is_201(self):
        checkout = self.find_expected_checkout(code=201)

        self.assertTrue(checkout.is_ready())

    def test_is_ready_returns_false_when_status_is_202(self):
        checkout = self.find_expected_checkout(code=202)

        self.assertFalse(checkout.is_ready())

    def test_find_payments_for_checkout(self):
        checkout = self.find_expected_checkout()

        self.fake(
            "checkouts/%s/payments" % self.expected_checkout_id,
            method='GET',
            code=200,
            body=self.load_fixture('payments')
        )
        payments = checkout.payments()
        self.assertEqual(10.00, payments[0].amount)

    def test_find_shipping_rates_for_checkout(self):
        checkout = self.find_expected_checkout()

        self.fake(
            "checkouts/%s/shipping_rates" % self.expected_checkout_id,
            method='GET',
            code=200,
            body=self.load_fixture('shipping_rates')
        )
        shipping_rates = checkout.shipping_rates()
        self.assertEqual("canada_post-INT.TP.BOGUS-4.00", shipping_rates[0].id)
