import shopify
from test_helper import TestCase

class RecurringApplicationChargeTest(TestCase):
    def test_activate_charge(self):
        # Just check that calling activate doesn't raise an exception.
        self.fake("recurring_application_charges/35463/activate", method='POST',headers={'Content-length':'0', 'Content-type': 'application/json'}, body=" ")
        charge = shopify.RecurringApplicationCharge({'id': 35463})
        charge.activate()
