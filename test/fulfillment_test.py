import shopify
from test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource

class FulFillmentTest(TestCase):
  
    def setUp(self):
        super(FulFillmentTest, self).setUp()
        self.fake("orders/450789469/fulfillments/255858046", method = 'GET', body = self.load_fixture('fulfillment'))

    def test_able_to_complete_fulfillment(self):
        fulfillment = shopify.Fulfillment.find(255858046, order_id = 450789469)

        success = self.load_fixture('fulfillment')
        success = success.replace('pending','success')
        self.fake("orders/450789469/fulfillments/255858046/complete", method = 'POST', headers = {'Content-length':'0', 'Content-type': 'application/json'}, body = success)

        self.assertEqual('pending', fulfillment.status)
        fulfillment.complete()
        self.assertEqual('success', fulfillment.status)
    
    def test_able_to_cancel_fulfillment(self):
        fulfillment = shopify.Fulfillment.find(255858046, order_id = 450789469)

        cancelled = self.load_fixture('fulfillment')
        cancelled = cancelled.replace('pending', 'cancelled')
        self.fake("orders/450789469/fulfillments/255858046/cancel", method = 'POST', headers = {'Content-length':'0', 'Content-type': 'application/json'}, body = cancelled)

        self.assertEqual('pending', fulfillment.status)
        fulfillment.cancel()
        self.assertEqual('cancelled', fulfillment.status)
