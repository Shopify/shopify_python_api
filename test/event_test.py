import shopify
from test.test_helper import TestCase

class EventTest(TestCase):
    def test_prefix_uses_resource(self):
        prefix = shopify.Event._prefix(options={'resource': "orders", "resource_id": 42})
        self.assertEqual("https://this-is-my-test-show.myshopify.com/admin/api/unstable/orders/42", prefix)

    def test_prefix_doesnt_need_resource(self):
        prefix = shopify.Event._prefix()
        self.assertEqual("https://this-is-my-test-show.myshopify.com/admin/api/unstable", prefix)
