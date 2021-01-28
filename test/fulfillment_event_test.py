import shopify
from test.test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource

class FulFillmentEventTest(TestCase):
    def setUp(self):
        super(FulFillmentEventTest, self).setUp()
        self.fake("orders/2776493818019/fulfillments/2608403447971/events", method='GET', body=self.load_fixture('fulfillment_event'))
        self.fulfillment_event = shopify.FulfillmentEvent.find(order_id=2776493818019, fulfillment_id=2608403447971)
    
    def test_get_fulfillment_event(self):
        self.assertEqual(1, len(self.fulfillment_event))

    def test_create_fulfillment_event(self):
        pass

    def test_error_on_incorrect_status(self):
        with self.assertRaises(AttributeError):
            self.fake("orders/2776493818019/fulfillments/2608403447971/events", method='PUT', body=self.load_fixture('article'), headers={'Content-type': 'application/json'})
            self.fulfillment_event.save()
