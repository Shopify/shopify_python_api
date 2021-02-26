import shopify
from test.test_helper import TestCase


class FulfillmentServiceTest(TestCase):
    def test_create_new_fulfillment_service(self):
        self.fake(
            "fulfillment_services",
            method='POST',
            body=self.load_fixture('fulfillment_service'),
            headers={'Content-type': 'application/json'},
        )

        fulfillment_service = shopify.FulfillmentService.create({'name': "SomeService"})
        self.assertEqual("SomeService", fulfillment_service.name)

    def test_get_fulfillment_service(self):
        self.fake("fulfillment_services/123456", method='GET', body=self.load_fixture('fulfillment_service'))

        fulfillment_service = shopify.FulfillmentService.find(123456)
        self.assertEqual("SomeService", fulfillment_service.name)

    def test_set_format_attribute(self):
        fulfillment_service = shopify.FulfillmentService()
        fulfillment_service.format = "json"
        self.assertEqual("json", fulfillment_service.attributes['format'])
