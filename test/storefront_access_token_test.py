import shopify
from test.test_helper import TestCase

class StorefrontAccessTokenTest(TestCase):
    def test_create_storefront_access_token(self):
        self.fake('storefront_access_tokens', method='POST', body=self.load_fixture('storefront_access_token'), headers={ 'Content-type': 'application/json' })
        storefront_access_token = shopify.StorefrontAccessToken.create({'title': 'Test'})
        self.assertEqual(1, storefront_access_token.id)
        self.assertEqual("Test", storefront_access_token.title)

    def test_get_and_delete_storefront_access_token(self):
        self.fake('storefront_access_tokens/1', method='GET', code=200, body=self.load_fixture('storefront_access_token'))
        storefront_access_token = shopify.StorefrontAccessToken.find(1)

        self.fake('storefront_access_tokens/1', method='DELETE', code=200, body='destroyed')
        storefront_access_token.destroy()
        self.assertEqual('DELETE', self.http.request.get_method())

    def test_get_storefront_access_tokens(self):
        self.fake('storefront_access_tokens', method='GET', code=200, body=self.load_fixture('storefront_access_tokens'))
        tokens = shopify.StorefrontAccessToken.find()

        self.assertEqual(2, len(tokens))
        self.assertEqual(1, tokens[0].id)
        self.assertEqual(2, tokens[1].id)
        self.assertEqual("Test 1", tokens[0].title)
        self.assertEqual("Test 2", tokens[1].title)
