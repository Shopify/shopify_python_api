import shopify
from test.test_helper import TestCase


class UsageChargeTest(TestCase):
    def test_create_usage_charge(self):
        self.fake("recurring_application_charges/654381177/usage_charges", method='POST',
                  body=self.load_fixture('usage_charge'), headers={'Content-type': 'application/json'})

        charge = shopify.UsageCharge({'price': 9.0, 'description': '1000 emails',
                                     'recurring_application_charge_id': 654381177})
        charge.save()
        self.assertEqual('1000 emails', charge.description)

    def test_get_usage_charge(self):
        self.fake("recurring_application_charges/654381177/usage_charges/359376002",
                  method='GET', body=self.load_fixture('usage_charge'))

        charge = shopify.UsageCharge.find(359376002, recurring_application_charge_id=654381177)
        self.assertEqual('1000 emails', charge.description)
