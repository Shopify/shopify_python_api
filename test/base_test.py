import shopify
from test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource
from mock import patch
import threading

class BaseTest(TestCase):

    @classmethod
    def setUpClass(self):
        self.session1 = shopify.Session('shop1.myshopify.com', 'token1')
        self.session2 = shopify.Session('shop2.myshopify.com', 'token2')

    def setUp(self):
        super(BaseTest, self).setUp()

    def tearDown(self):
        shopify.ShopifyResource.clear_session()

    def test_activate_session_should_set_site_and_headers_for_given_session(self):
        shopify.ShopifyResource.activate_session(self.session1)

        self.assertIsNone(ActiveResource.site)
        self.assertEqual('https://shop1.myshopify.com/admin', shopify.ShopifyResource.site)
        self.assertEqual('https://shop1.myshopify.com/admin', shopify.Shop.site)
        self.assertIsNone(ActiveResource.headers)
        self.assertEqual('token1', shopify.ShopifyResource.headers['X-Shopify-Access-Token'])
        self.assertEqual('token1', shopify.Shop.headers['X-Shopify-Access-Token'])

    def test_clear_session_should_clear_site_and_headers_from_Base(self):
        shopify.ShopifyResource.activate_session(self.session1)
        shopify.ShopifyResource.clear_session()

        self.assertIsNone(ActiveResource.site)
        self.assertIsNone(shopify.ShopifyResource.site)
        self.assertIsNone(shopify.Shop.site)

        self.assertIsNone(ActiveResource.headers)
        self.assertFalse('X-Shopify-Access-Token' in shopify.ShopifyResource.headers)
        self.assertFalse('X-Shopify-Access-Token' in shopify.Shop.headers)

    def test_activate_session_with_one_session_then_clearing_and_activating_with_another_session_shoul_request_to_correct_shop(self):
        shopify.ShopifyResource.activate_session(self.session1)
        shopify.ShopifyResource.clear_session
        shopify.ShopifyResource.activate_session(self.session2)

        self.assertIsNone(ActiveResource.site)
        self.assertEqual('https://shop2.myshopify.com/admin', shopify.ShopifyResource.site)
        self.assertEqual('https://shop2.myshopify.com/admin', shopify.Shop.site)

        self.assertIsNone(ActiveResource.headers)
        self.assertEqual('token2', shopify.ShopifyResource.headers['X-Shopify-Access-Token'])
        self.assertEqual('token2', shopify.Shop.headers['X-Shopify-Access-Token'])

    def test_delete_should_send_custom_headers_with_request(self):
        shopify.ShopifyResource.activate_session(self.session1)

        org_headers=shopify.ShopifyResource.headers
        shopify.ShopifyResource.set_headers({'X-Custom': 'abc'})

        with patch('shopify.ShopifyResource.connection.delete') as mock:
            shopify.ShopifyResource.delete('1')
            mock.assert_called_with('/admin/shopify_resources/1.json', {'X-Custom': 'abc'})

        shopify.ShopifyResource.set_headers(org_headers)

    def test_headers_includes_user_agent(self):
        self.assertTrue('User-Agent' in shopify.ShopifyResource.headers)
        t = threading.Thread(target=lambda: self.assertTrue('User-Agent' in shopify.ShopifyResource.headers))
        t.start()
        t.join()

    def test_headers_is_thread_safe(self):
        def testFunc():
            shopify.ShopifyResource.headers['X-Custom'] = 'abc'
            self.assertTrue('X-Custom' in shopify.ShopifyResource.headers)

        t1 = threading.Thread(target=testFunc)
        t1.start()
        t1.join()

        t2 = threading.Thread(target=lambda: self.assertFalse('X-Custom' in shopify.ShopifyResource.headers))
        t2.start()
        t2.join()
