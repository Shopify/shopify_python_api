import shopify
from test.test_helper import TestCase

class RecurringApplicationChargeTest(TestCase):
    def test_activate_charge(self):
        # Just check that calling activate doesn't raise an exception.
        self.fake("recurring_application_charges/35463/activate", method='POST',headers={'Content-length':'0', 'Content-type': 'application/json'}, body=" ")
        charge = shopify.RecurringApplicationCharge({'id': 35463})
        charge.activate()

    def test_current_method_returns_active_charge(self):
        # Test that current() class method correctly returns
        # first RecurringApplicationCharge with active status
        self.fake("recurring_application_charges")
        charge = shopify.RecurringApplicationCharge.current()
        self.assertEqual(charge.id, 455696195)

    def test_current_method_returns_none_if_active_not_found(self):
        # Test that current() class method correctly returns
        # None if RecurringApplicationCharge with active status not found
        self.fake("recurring_application_charges", body=self.load_fixture("recurring_application_charges_no_active"))
        charge = shopify.RecurringApplicationCharge.current()
        self.assertEqual(charge, None)

    def test_usage_charges_method_returns_associated_usage_charges(self):
        self.fake("recurring_application_charges")
        charge = shopify.RecurringApplicationCharge.current()

        self.fake("recurring_application_charges/455696195/usage_charges", method='GET', body=self.load_fixture('usage_charges'))
        usage_charges = charge.usage_charges()
        self.assertEqual(len(usage_charges), 2)

    def test_customize_method_increases_capped_amount(self):
        self.fake("recurring_application_charges")
        charge = shopify.RecurringApplicationCharge.current()
        self.assertEqual(charge.capped_amount, 100)

        self.fake("recurring_application_charges/455696195/customize.json?recurring_application_charge%5Bcapped_amount%5D=200", extension=False, method='PUT', headers={'Content-length':'0', 'Content-type': 'application/json'}, body=self.load_fixture('recurring_application_charge_adjustment'))
        charge.customize(capped_amount= 200)
        self.assertTrue(charge.update_capped_amount_url)

    def test_destroy_recurring_application_charge(self):
        self.fake('recurring_application_charges')
        charge = shopify.RecurringApplicationCharge.current()

        self.fake('recurring_application_charges/455696195', method='DELETE', body='{}')
        charge.destroy()
