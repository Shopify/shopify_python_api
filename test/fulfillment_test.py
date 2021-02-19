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

    def test_update_tracking(self):
        fulfillment = shopify.Fulfillment.find(255858046, order_id=450789469)

        tracking_info = { "number": 1111, "url": "http://www.my-url.com", "company": "my-company"}
        notify_customer = False

        update_tracking = self.load_fixture('fulfillment')
        update_tracking = update_tracking.replace(b'null-company', b'my-company')
        update_tracking = update_tracking.replace(b'http://www.google.com/search?q=1Z2345', b'http://www.my-url.com')
        update_tracking = update_tracking.replace(b'1Z2345', b'1111')

        self.fake("fulfillments/255858046/update_tracking", method="POST", headers={'Content-type': 'application/json'}, body=update_tracking)

        self.assertEqual("null-company", fulfillment.tracking_company)
        self.assertEqual("1Z2345", fulfillment.tracking_number)
        self.assertEqual("http://www.google.com/search?q=1Z2345", fulfillment.tracking_url)
        fulfillment.update_tracking(tracking_info, notify_customer)
        self.assertEqual("my-company", fulfillment.tracking_company)
        self.assertEqual('1111', fulfillment.tracking_number)
        self.assertEqual('http://www.my-url.com', fulfillment.tracking_url)
