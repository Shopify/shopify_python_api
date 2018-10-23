import shopify
from test.test_helper import TestCase

class CurrencyTest(TestCase):

    def test_get_currencies(self):
        self.fake('currencies', method='GET', code=200, body=self.load_fixture('currencies'))

        currencies = shopify.Currency.find()
        self.assertEqual(4, len(currencies))
        self.assertEqual("AUD", currencies[0].currency)
        self.assertEqual("2018-10-03T14:44:08-04:00", currencies[0].rate_updated_at)
        self.assertEqual(True, currencies[0].enabled)
        self.assertEqual("EUR", currencies[1].currency)
        self.assertEqual("2018-10-03T14:44:08-04:00", currencies[1].rate_updated_at)
        self.assertEqual(True, currencies[1].enabled)
        self.assertEqual("GBP", currencies[2].currency)
        self.assertEqual("2018-10-03T14:44:08-04:00", currencies[2].rate_updated_at)
        self.assertEqual(True, currencies[2].enabled)
        self.assertEqual("HKD", currencies[3].currency)
        self.assertEqual("2018-10-03T14:44:08-04:00", currencies[3].rate_updated_at)
        self.assertEqual(False, currencies[3].enabled)

