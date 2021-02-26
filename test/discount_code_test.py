import shopify
import json
from test.test_helper import TestCase


class DiscountCodeTest(TestCase):
    def setUp(self):
        super(DiscountCodeTest, self).setUp()
        self.fake("price_rules/1213131/discount_codes/34", method='GET', body=self.load_fixture('discount_code'))
        self.discount_code = shopify.DiscountCode.find(34, price_rule_id=1213131)

    def test_find_a_specific_discount_code(self):
        discount_code = shopify.DiscountCode.find(34, price_rule_id=1213131)
        self.assertEqual("25OFF", discount_code.code)

    def test_update_a_specific_discount_code(self):
        self.discount_code.code = 'BOGO'
        self.fake(
            'price_rules/1213131/discount_codes/34',
            method='PUT',
            code=200,
            body=self.load_fixture('discount_code'),
            headers={'Content-type': 'application/json'},
        )
        self.discount_code.save()
        self.assertEqual('BOGO', json.loads(self.http.request.data.decode("utf-8"))["discount_code"]["code"])

    def test_delete_a_specific_discount_code(self):
        self.fake('price_rules/1213131/discount_codes/34', method='DELETE', body='destroyed')
        self.discount_code.destroy()
        self.assertEqual('DELETE', self.http.request.get_method())
