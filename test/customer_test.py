import shopify
from test.test_helper import TestCase

class CustomerTest(TestCase):

    def test_search(self):
        self.fake("customers/search.json?query=Bob+country%3AUnited+States", extension=False, body=self.load_fixture('customers_search'))

        results = shopify.Customer.search(query='Bob country:United States')
        self.assertEqual('Bob', results[0].first_name)
