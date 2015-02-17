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
