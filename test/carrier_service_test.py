import shopify
from test.test_helper import TestCase


class CarrierServiceTest(TestCase):
    def test_create_new_carrier_service(self):
        self.fake("carrier_services", method='POST', body=self.load_fixture(
            'carrier_service'), headers={'Content-type': 'application/json'})

        carrier_service = shopify.CarrierService.create({'name': "Some Postal Service"})
        self.assertEqual("Some Postal Service", carrier_service.name)

    def test_get_carrier_service(self):
        self.fake("carrier_services/123456", method='GET', body=self.load_fixture('carrier_service'))

        carrier_service = shopify.CarrierService.find(123456)
        self.assertEqual("Some Postal Service", carrier_service.name)

    def test_set_format_attribute(self):
        carrier_service = shopify.CarrierService()
        carrier_service.format = "json"
        self.assertEqual("json", carrier_service.attributes['format'])
