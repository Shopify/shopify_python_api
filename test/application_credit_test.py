import shopify
from test.test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource

class ApplicationCreditTest(TestCase):
    def test_get_application_credit(self):
        self.fake("application_credits/445365009", method='GET', body=self.load_fixture('application_credit'))
        application_credit = shopify.ApplicationCredit.find(445365009)
        self.assertEqual('5.00', application_credit.amount)

    def test_get_all_application_credits(self):
        self.fake("application_credits", method='GET', body=self.load_fixture('application_credits'))
        application_credits = shopify.ApplicationCredit.find()
        self.assertEqual(1, len(application_credits))
        self.assertEqual(445365009, application_credits[0].id)
