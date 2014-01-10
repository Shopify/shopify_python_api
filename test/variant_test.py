import shopify
from test_helper import TestCase

class VariantTest(TestCase):

    def test_get_variants(self):
        self.fake("products/632910392/variants", method = 'GET', body = self.load_fixture('variants'))
        v = shopify.Variant.find(product_id = 632910392)

    def test_get_variant_namespaced(self):
        self.fake("products/632910392/variants/808950810", method = 'GET', body = self.load_fixture('variant'))
        v = shopify.Variant.find(808950810, product_id = 632910392)

    def test_get_variant(self):
        # fix extra slash from pyactiveresource
        self.fake("/variants/808950810", method = 'GET', body = self.load_fixture('variant'))
        v = shopify.Variant.find(808950810)
