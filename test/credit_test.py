import shopify
from test.test_helper import TestCase

class ApplicationCreditTest(TestCase):
    def test_create_application_credit(self):
        self.fake("application_credits", method='POST', body=self.load_fixture('credit'), headers={'Content-type': 'application/json'})

        credit = shopify.ApplicationCharge()
        credit.test =True
        credit.description = "application credit for refund"
        credit.amount = 5.0
        credit.save()
        self.assertEqual("application credit for refund",credit.description)
    
    def test_get_application_credit(self):
        self.assertEqual("application credit for refund",credit.description)