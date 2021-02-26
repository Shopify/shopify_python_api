import shopify
from test.test_helper import TestCase


class CheckoutTest(TestCase):
    def test_all_should_return_all_checkouts(self):
        self.fake('checkouts')
        checkouts = shopify.Checkout.find()
        self.assertEqual(1, len(checkouts))
        self.assertEqual(450789469, checkouts[0].id)
        self.assertEqual("2a1ace52255252df566af0faaedfbfa7", checkouts[0].token)
        self.assertEqual(2, len(checkouts[0].line_items))
