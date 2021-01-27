import shopify
from test.test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource

class FulFillmentEventTest(TestCase):
  def setUp(self):
    super(FulFillmentEventTest, self).setUp()
    self.fake("orders/450789469/fulfillments/255858046/events", method='GET', body=self.load_fixture('fulfillment_event'))
    
  def test_get_fulfillment_event(self):
    fulfillment_event = shopify.FulfillmentEvent.find(order_id='450789469', fulfillment_id='255858046')
    self.assertEqual(1, len(fulfillment_event))

  # def test_create_fulfillment_event(self):


  def test_error_on_incorrect_status(self):
    with self.assertRaises(AttributeError):
      incorrect_status = 'asdf'
      fulfillment_event = shopify.FulfillmentEvent.find(order_id='450789469', fulfillment_id='255858046')
      fulfillment_event.status = incorrect_status
      fulfillment_event.save()
