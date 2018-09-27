import shopify
from test.test_helper import TestCase

class AccessScopeTest(TestCase):

  def test_all_should_return_all_checkouts(self):
    self.fake('access_scopes')
    scopes = shopify.AccessScope.find()
    self.assertEqual(3, len(scopes))
    self.assertEqual('read_products', scopes[0].handle)
