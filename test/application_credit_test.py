import shopify
import json
from test.test_helper import TestCase


class ApplicationCreditTest(TestCase):
    def test_get_application_credit(self):
        self.fake('application_credits/445365009', method='GET', body=self.load_fixture('application_credit'), code=200)
        application_credit = shopify.ApplicationCredit.find(445365009)
        self.assertEqual('5.00', application_credit.amount)

    def test_get_all_application_credits(self):
        self.fake('application_credits', method='GET', body=self.load_fixture('application_credits'), code=200)
        application_credits = shopify.ApplicationCredit.find()
        self.assertEqual(1, len(application_credits))
        self.assertEqual(445365009, application_credits[0].id)

    def test_create_application_credit(self):
        self.fake(
            'application_credits',
            method='POST',
            body=self.load_fixture('application_credit'),
            headers={'Content-type': 'application/json'},
            code=201
        )

        application_credit = shopify.ApplicationCredit.create({
            'description': 'application credit for refund',
            'amount': 5.0
        })

        expected_body = {
            "application_credit": {
                "description": "application credit for refund",
                "amount": 5.0
            }
        }

        self.assertEqual(expected_body, json.loads(self.http.request.data.decode("utf-8")))
