import shopify
import json
from test.test_helper import TestCase


class CustomerTest(TestCase):
    def setUp(self):
        super(CustomerTest, self).setUp()
        self.fake("customers/207119551", method="GET", body=self.load_fixture("customer"))
        self.customer = shopify.Customer.find(207119551)

    def test_create_customer(self):
        self.fake(
            "customers", method="POST", body=self.load_fixture("customer"), headers={"Content-type": "application/json"}
        )
        customer = shopify.Customer()
        customer.first_name = "Bob"
        customer.last_name = "Lastnameson"
        customer.email = "steve.lastnameson@example.com"
        customer.verified_email = True
        customer.password = "newpass"
        customer.password_confirmation = "newpass"
        self.assertEqual("newpass", customer.attributes["password"])
        customer.save()
        self.assertEqual("Bob", customer.first_name)
        self.assertEqual("newpass", customer.attributes["password"])

    def test_get_customer(self):
        self.assertEqual("Bob", self.customer.first_name)

    def test_search(self):
        self.fake(
            "customers/search.json?query=Bob+country%3AUnited+States",
            extension=False,
            body=self.load_fixture("customers_search"),
        )

        results = shopify.Customer.search(query="Bob country:United States")
        self.assertEqual("Bob", results[0].first_name)

    def test_send_invite_with_no_params(self):
        customer_invite_fixture = self.load_fixture("customer_invite")
        customer_invite = json.loads(customer_invite_fixture.decode("utf-8"))
        self.fake(
            "customers/207119551/send_invite",
            method="POST",
            body=customer_invite_fixture,
            headers={"Content-type": "application/json"},
        )
        customer_invite_response = self.customer.send_invite()
        self.assertEqual(json.loads('{"customer_invite": {}}'), json.loads(self.http.request.data.decode("utf-8")))
        self.assertIsInstance(customer_invite_response, shopify.CustomerInvite)
        self.assertEqual(customer_invite["customer_invite"]["to"], customer_invite_response.to)

    def test_send_invite_with_params(self):
        customer_invite_fixture = self.load_fixture("customer_invite")
        customer_invite = json.loads(customer_invite_fixture.decode("utf-8"))
        self.fake(
            "customers/207119551/send_invite",
            method="POST",
            body=customer_invite_fixture,
            headers={"Content-type": "application/json"},
        )
        customer_invite_response = self.customer.send_invite(shopify.CustomerInvite(customer_invite["customer_invite"]))
        self.assertEqual(customer_invite, json.loads(self.http.request.data.decode("utf-8")))
        self.assertIsInstance(customer_invite_response, shopify.CustomerInvite)
        self.assertEqual(customer_invite["customer_invite"]["to"], customer_invite_response.to)

    def test_get_customer_orders(self):
        self.fake("customers/207119551", method="GET", body=self.load_fixture("customer"))
        customer = shopify.Customer.find(207119551)
        self.fake("customers/207119551/orders", method="GET", body=self.load_fixture("orders"))
        orders = customer.orders()
        self.assertIsInstance(orders[0], shopify.Order)
        self.assertEqual(450789469, orders[0].id)
        self.assertEqual(207119551, orders[0].customer.id)
