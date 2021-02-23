from test.test_helper import TestCase
import shopify


class DiscountCodeCreationTest(TestCase):
    def test_find_batch_job_discount_codes(self):
        self.fake('price_rules/1213131', body=self.load_fixture('price_rule'))
        price_rule = shopify.PriceRule.find(1213131)

        self.fake('price_rules/1213131/batch/989355119', body=self.load_fixture('discount_code_creation'))
        batch = price_rule.find_batch(989355119)

        self.fake('price_rules/1213131/batch/989355119/discount_codes', body=self.load_fixture('batch_discount_codes'))
        discount_codes = batch.discount_codes()

        self.assertEqual('foo', discount_codes[0].code)
        self.assertEqual('bar', discount_codes[2].code)
