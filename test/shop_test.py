import shopify
from test_helper import TestCase

class ShopTest(TestCase):
    def setUp(self):
        super(ShopTest, self).setUp()
        self.fake("shop")
        self.shop = shopify.Shop.current()

    def test_current_should_return_current_shop(self):
        self.assertTrue(isinstance(self.shop,shopify.Shop))
        self.assertEqual("Apple Computers", self.shop.name)
        self.assertEqual("apple.myshopify.com", self.shop.myshopify_domain)
        self.assertEqual(690933842, self.shop.id)
        self.assertEqual("2007-12-31T19:00:00-05:00", self.shop.created_at)
        self.assertIsNone(self.shop.tax_shipping)

    def test_get_metafields_for_shop(self):
        self.fake("metafields")

        metafields = self.shop.metafields()

        self.assertEqual(2, len(metafields))
        for field in metafields:
            self.assertTrue(isinstance(field, shopify.Metafield))

    def test_add_metafield(self):
        self.fake("metafields", method='POST', code=201, body=self.load_fixture('metafield'), headers={'Content-type': 'application/json'})

        field = self.shop.add_metafield( shopify.Metafield({'namespace': "contact", 'key': "email", 'value': "123@example.com", 'value_type': "string"}))

        self.assertFalse(field.is_new())
        self.assertEqual("contact", field.namespace)
        self.assertEqual("email", field.key)
        self.assertEqual("123@example.com", field.value)

    def test_events(self):
        self.fake("events")

        events = self.shop.events()

        self.assertEqual(3, len(events))
        for event in events:
            self.assertTrue(isinstance(event, shopify.Event))
