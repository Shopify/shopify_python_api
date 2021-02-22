import shopify
from test.test_helper import TestCase


class ProductTest(TestCase):

    def setUp(self):
        super(ProductTest, self).setUp()

        self.fake("products/632910392", body=self.load_fixture('product'))
        self.product = shopify.Product.find(632910392)

    def test_add_metafields_to_product(self):
        self.fake("products/632910392/metafields", method='POST', code=201,
                  body=self.load_fixture('metafield'), headers={'Content-type': 'application/json'})

        field = self.product.add_metafield(shopify.Metafield(
            {'namespace': "contact", 'key': "email", 'value': "123@example.com", 'value_type': "string"}))

        self.assertFalse(field.is_new())
        self.assertEqual("contact", field.namespace)
        self.assertEqual("email", field.key)
        self.assertEqual("123@example.com", field.value)

    def test_get_metafields_for_product(self):
        self.fake("products/632910392/metafields", body=self.load_fixture('metafields'))

        metafields = self.product.metafields()

        self.assertEqual(2, len(metafields))
        for field in metafields:
            self.assertTrue(isinstance(field, shopify.Metafield))

    def test_get_metafields_for_product_with_params(self):
        self.fake("products/632910392/metafields.json?limit=2", extension=False, body=self.load_fixture('metafields'))

        metafields = self.product.metafields(limit=2)
        self.assertEqual(2, len(metafields))
        for field in metafields:
            self.assertTrue(isinstance(field, shopify.Metafield))

    def test_get_metafields_for_product_count(self):
        self.fake("products/632910392/metafields/count", body=self.load_fixture('metafields_count'))

        metafields_count = self.product.metafields_count()
        self.assertEqual(2, metafields_count)

    def test_get_metafields_for_product_count_with_params(self):
        self.fake("products/632910392/metafields/count.json?value_type=string",
                  extension=False, body=self.load_fixture('metafields_count'))

        metafields_count = self.product.metafields_count(value_type="string")
        self.assertEqual(2, metafields_count)

    def test_update_loaded_variant(self):
        self.fake("products/632910392/variants/808950810", method='PUT', code=200, body=self.load_fixture('variant'))

        variant = self.product.variants[0]
        variant.price = "0.50"
        variant.save

    def test_add_variant_to_product(self):
        self.fake("products/632910392/variants", method='POST',
                  body=self.load_fixture('variant'), headers={'Content-type': 'application/json'})
        self.fake("products/632910392/variants/808950810", method='PUT', code=200,
                  body=self.load_fixture('variant'), headers={'Content-type': 'application/json'})
        v = shopify.Variant()
        self.assertTrue(self.product.add_variant(v))
