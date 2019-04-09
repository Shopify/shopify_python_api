import shopify
from test.test_helper import TestCase

class AccessScopeTest(TestCase):

  def test_find_should_return_all_access_scopes(self):
    self.fake('oauth/access_scopes', body=self.load_fixture('access_scopes'),
        prefix='/admin')
    scopes = shopify.AccessScope.find()
    self.assertEqual(3, len(scopes))
    self.assertEqual('read_products', scopes[0].handle)
