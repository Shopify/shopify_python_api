import shopify
from test.test_helper import TestCase


class CustomerSavedSearchTest(TestCase):
    def setUp(self):
        super(CustomerSavedSearchTest, self).setUp()
        self.load_customer_saved_search()

    def test_get_customers_from_customer_saved_search(self):
        self.fake(
            "customer_saved_searches/8899730/customers", body=self.load_fixture("customer_saved_search_customers")
        )
        self.assertEqual(1, len(self.customer_saved_search.customers()))
        self.assertEqual(112223902, self.customer_saved_search.customers()[0].id)

    def test_get_customers_from_customer_saved_search_with_params(self):
        self.fake(
            "customer_saved_searches/8899730/customers.json?limit=1",
            extension=False,
            body=self.load_fixture("customer_saved_search_customers"),
        )
        customers = self.customer_saved_search.customers(limit=1)
        self.assertEqual(1, len(customers))
        self.assertEqual(112223902, customers[0].id)

    def load_customer_saved_search(self):
        self.fake("customer_saved_searches/8899730", body=self.load_fixture("customer_saved_search"))
        self.customer_saved_search = shopify.CustomerSavedSearch.find(8899730)
