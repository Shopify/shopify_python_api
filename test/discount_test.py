import shopify
from test.test_helper import TestCase


class DiscountTest(TestCase):

    def test_discount_creation(self):
        self.fake('discounts',
                  method='POST',
                  code=202,
                  body=self.load_fixture('discount'),
                  headers={'Content-type': 'application/json'})
        discount = shopify.Discount.create({
            "discount_type": "shipping",
            "code": "quidagis?",
            "starts_at": "2015-08-23T00:00:00-04:00",
            "ends_at": "2015-08-27T23:59:59-04:00",
            "usage_limit": 20
        })
        self.assertEqual("shipping", discount.discount_type)
        self.assertEqual("quidagis?", discount.code)

    def test_fetch_discounts(self):
        self.fake('discounts',
                  method='GET',
                  code=200,
                  body=self.load_fixture('discounts'))
        discounts = shopify.Discount.find()
        self.assertEqual(2, len(discounts))

    def test_disable_discount(self):
        self.fake('discounts/992807812',
                  method='GET',
                  code=200,
                  body=self.load_fixture('discounts'))
        self.fake('discounts/992807812/disable',
                  method='POST',
                  code=200,
                  body=self.load_fixture('discount_disabled'),
                  headers={'Content-length': '0',
                           'Content-type': 'application/json'})
        discount = shopify.Discount.find(992807812)
        self.assertEqual("enabled", discount.status)
        discount.disable()
        self.assertEqual("disabled", discount.status)
