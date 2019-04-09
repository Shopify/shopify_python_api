import shopify
from test.test_helper import TestCase

class VariantTest(TestCase):

    def test_get_variants(self):
        self.fake("products/632910392/variants", method='GET', body=self.load_fixture('variants'))
        v = shopify.Variant.find(product_id = 632910392)

    def test_get_variant_namespaced(self):
        self.fake("products/632910392/variants/808950810", method='GET', body=self.load_fixture('variant'))
        v = shopify.Variant.find(808950810, product_id = 632910392)

    def test_update_variant_namespace(self):
        self.fake("products/632910392/variants/808950810", method='GET', body=self.load_fixture('variant'))
        v = shopify.Variant.find(808950810, product_id = 632910392)

        self.fake("products/632910392/variants/808950810", method='PUT', body=self.load_fixture('variant'), headers={'Content-type': 'application/json'})
        v.save()

    def test_create_variant(self):
        self.fake("products/632910392/variants", method='POST', body=self.load_fixture('variant'), headers={'Content-type': 'application/json'})
        v = shopify.Variant({'product_id':632910392})
        v.save()

    def test_create_variant_then_add_parent_id(self):
        self.fake("products/632910392/variants", method='POST', body=self.load_fixture('variant'), headers={'Content-type': 'application/json'})
        v = shopify.Variant()
        v.product_id = 632910392
        v.save()

    def test_get_variant(self):
        self.fake("variants/808950810", method='GET', body=self.load_fixture('variant'))
        v = shopify.Variant.find(808950810)
