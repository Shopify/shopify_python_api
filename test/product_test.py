from test_helper import *

class ProductTest(TestCase):
  
    def setUp(self):
        super(ProductTest, self).setUp()

        self.fake("products/632910392", body = self.load_fixture('product'))
        self.product = shopify.Product.find(632910392)

    def test_add_metafields_to_product(self):
        self.fake("products/632910392/metafields", method = 'POST', code = 201, body = self.load_fixture('metafield'))

        field = self.product.add_metafield(shopify.Metafield({'namespace': "contact", 'key': "email", 'value': "123@example.com", 'value_type': "string"}))

        self.assertFalse(field.is_new())
        self.assertEqual("contact", field.namespace)
        self.assertEqual("email", field.key)
        self.assertEqual("123@example.com", field.value)

    def test_get_metafields_for_product(self):
        self.fake("products/632910392/metafields", body = self.load_fixture('metafields'))

        metafields = self.product.metafields()

        self.assertEqual(2, len(metafields))
        for field in metafields:
            self.assertTrue(isinstance(field, shopify.Metafield))

    def test_update_loaded_variant(self):
        self.fake("products/632910392/variants/808950810", method = 'PUT', code = 200, body = self.load_fixture('variant'))

        variant = self.product.variants[0]
        variant.price = "0.50"
        variant.save
