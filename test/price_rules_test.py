import json
from test.test_helper import TestCase

import shopify


class PriceRuleTest(TestCase):

    def setUp(self):
        super(PriceRuleTest, self).setUp()
        self.fake('price_rules/1213131', body=self.load_fixture('price_rule'))
        self.price_rule = shopify.PriceRule.find(1213131)

    def test_get_price_rule(self):
        self.fake('price_rule/1213131', method='GET', status=200, body=self.load_fixture('price_rule'))
        price_rule = shopify.PriceRule.find(1213131)
        self.assertEqual(1213131, price_rule.id)

    def test_get_all_price_rules(self):
        self.fake('price_rules',
                  method='GET',
                  code=200,
                  body=self.load_fixture('price_rules'))
        price_rules = shopify.PriceRule.find()
        self.assertEqual(2, len(price_rules))

    def test_update_price_rule(self):
        self.price_rule.title = "Buy One Get One"
        self.fake('price_rules/1213131', method='PUT', status=200, body=self.load_fixture('price_rule'), headers={'Content-type': 'application/json'})
        self.price_rule.save()
        self.assertEqual('Buy One Get One', json.loads(self.http.request.data.decode("utf-8"))['price_rule']['title'])


    def test_delete_price_rule(self):
        self.fake('price_rules/1213131', method='DELETE', body='destroyed')
        self.price_rule.destroy()
        self.assertEqual('DELETE', self.http.request.get_method())

    def test_price_rule_creation(self):
        self.fake('price_rules',
                  method='POST',
                  code=202,
                  body=self.load_fixture('price_rule'),
                  headers={'Content-type': 'application/json'})
        price_rule = shopify.PriceRule.create({
            "title": "BOGO",
            "target_type": "line_item",
            "target_selection": "all",
            "allocation_method": "across",
            "value_type": "percentage",
            "value": -100,
            "once_per_customer": 'true',
            "customer_selection": 'all'
        })
        self.assertEqual("BOGO", price_rule.title)
        self.assertEqual("line_item", price_rule.target_type)

    def test_get_discount_codes(self):
        self.fake('price_rules/1213131/discount_codes', method='GET', status=200, body=self.load_fixture('discount_codes'))
        discount_codes = self.price_rule.discount_codes()
        self.assertEqual(1, len(discount_codes))

    def test_add_discount_code(self):
        price_rule_discount_fixture = self.load_fixture('discount_code')
        discount_code = json.loads(price_rule_discount_fixture.decode("utf-8"))
        self.fake('price_rules/1213131/discount_codes',
                  method='POST', 
                  body=price_rule_discount_fixture, 
                  headers={'Content-type': 'application/json'})
        price_rule_discount_response = self.price_rule.add_discount(shopify.DiscountCode(discount_code['discount_code']))
        self.assertEqual(discount_code, json.loads(self.http.request.data.decode("utf-8")))
        self.assertIsInstance(price_rule_discount_response, shopify.DiscountCode)
        self.assertEqual(discount_code['discount_code']['code'], price_rule_discount_response.code)

