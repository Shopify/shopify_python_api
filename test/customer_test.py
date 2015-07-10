import shopify
from test.test_helper import TestCase

class CustomerTest(TestCase):

    def test_create_customer(self):
        self.fake("customers", method='POST', body=self.load_fixture('customer'), headers={'Content-type': 'application/json'})
        customer = shopify.Customer()
        customer.first_name = 'Bob'
        customer.last_name = 'Lastnameson'
        customer.email = 'steve.lastnameson@example.com'
        customer.verified_email = True
        customer.password = "newpass"
        customer.password_confirmation = "newpass"
        self.assertEqual("newpass", customer.attributes['password'])
        customer.save()
        self.assertEqual("Bob", customer.first_name)
        self.assertEqual("newpass", customer.attributes['password'])

    def test_get_customer(self):
        self.fake('customers/207119551', method='GET', body=self.load_fixture('customer'))
        customer = shopify.Customer.find(207119551)
        self.assertEqual("Bob", customer.first_name)

    def test_search(self):
        self.fake("customers/search.json?query=Bob+country%3AUnited+States", extension=False, body=self.load_fixture('customers_search'))

        results = shopify.Customer.search(query='Bob country:United States')
        self.assertEqual('Bob', results[0].first_name)
