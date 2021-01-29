import shopify
from test.test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource

class FulFillmentEventTest(TestCase):
    def test_get_fulfillment_event(self):
        self.fake("orders/2776493818019/fulfillments/2608403447971/events", method='GET', body=self.load_fixture('fulfillment_event'))
        fulfillment_event = shopify.FulfillmentEvent.find(order_id=2776493818019, fulfillment_id=2608403447971)
        self.assertEqual(1, len(fulfillment_event))

    def test_create_fulfillment_event(self):
        self.fake("orders/2776493818019/fulfillments/2608403447971/events", method='POST', body=self.load_fixture('fulfillment_event'), headers={'Content-type': 'application/json'})
        new_fulfillment_event = shopify.FulfillmentEvent({'order_id': '2776493818019', 'fulfillment_id': '2608403447971'})
        new_fulfillment_event.status = 'ready_for_pickup'
        new_fulfillment_event.save()

    def test_error_on_incorrect_status(self):
        with self.assertRaises(AttributeError):
            self.fake("orders/2776493818019/fulfillments/2608403447971/events/12584341209251", method='GET', body=self.load_fixture('fulfillment_event'))
            incorrect_status = 'asdf'
            fulfillment_event = shopify.FulfillmentEvent.find(12584341209251, order_id='2776493818019', fulfillment_id='2608403447971')
            fulfillment_event.status = incorrect_status
            fulfillment_event.save()

