import shopify
from test.test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource


class FulFillmentTest(TestCase):
  
    def setUp(self):
        super(FulFillmentTest, self).setUp()
        self.fake("orders/450789469/fulfillments/255858046", method='GET', body=self.load_fixture('fulfillment'))

    def test_able_to_open_fulfillment(self):
        fulfillment = shopify.Fulfillment.find(255858046, order_id=450789469)

        success = self.load_fixture('fulfillment')
        success = success.replace(b'pending',b'open')
        self.fake("orders/450789469/fulfillments/255858046/open", method='POST', headers={'Content-length':'0', 'Content-type': 'application/json'}, body=success)

        self.assertEqual('pending', fulfillment.status)
        fulfillment.open()
        self.assertEqual('open', fulfillment.status)

    def test_able_to_complete_fulfillment(self):
        fulfillment = shopify.Fulfillment.find(255858046, order_id=450789469)

        success = self.load_fixture('fulfillment')
        success = success.replace(b'pending',b'success')
        self.fake("orders/450789469/fulfillments/255858046/complete", method='POST', headers={'Content-length':'0', 'Content-type': 'application/json'}, body=success)

        self.assertEqual('pending', fulfillment.status)
        fulfillment.complete()
        self.assertEqual('success', fulfillment.status)
    
    def test_able_to_cancel_fulfillment(self):
        fulfillment = shopify.Fulfillment.find(255858046, order_id=450789469)

        cancelled = self.load_fixture('fulfillment')
        cancelled = cancelled.replace(b'pending', b'cancelled')
        self.fake("orders/450789469/fulfillments/255858046/cancel", method='POST', headers={'Content-length':'0', 'Content-type': 'application/json'}, body=cancelled)

        self.assertEqual('pending', fulfillment.status)
        fulfillment.cancel()
        self.assertEqual('cancelled', fulfillment.status)
