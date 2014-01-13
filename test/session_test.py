import shopify
from test_helper import TestCase
try:
    from hashlib import md5
except ImportError:
    from md5 import md5
import time

class SessionTest(TestCase):

    def test_not_be_valid_without_a_url(self):
        session = shopify.Session("", "any-token")
        self.assertFalse(session.valid)
    
    def test_not_be_valid_without_token(self):
        session = shopify.Session("testshop.myshopify.com")
        self.assertFalse(session.valid)

    def test_be_valid_with_any_token_and_any_url(self):
        session = shopify.Session("testshop.myshopify.com", "any-token")
        self.assertTrue(session.valid)
    
    def test_not_raise_error_without_params(self):
        session = shopify.Session("testshop.myshopify.com", "any-token")

    def test_raise_error_if_params_passed_but_signature_omitted(self):
        with self.assertRaises(Exception):
            session = shopify.Session("testshop.myshopify.com")
            token = session.request_token('code', {'foo': 'bar'})

    def test_setup_api_key_and_secret_for_all_sessions(self):
        shopify.Session.setup(api_key="My test key", secret="My test secret")
        self.assertEqual("My test key", shopify.Session.api_key)
        self.assertEqual("My test secret", shopify.Session.secret)
    
    def test_use_https_protocol_by_default_for_all_sessions(self):
        self.assertEqual('https', shopify.Session.protocol)

    def test_temp_reset_shopify_ShopifyResource_site_to_original_value(self):
        shopify.Session.setup(api_key="key", secret="secret")
        session1 = shopify.Session('fakeshop.myshopify.com', 'token1')
        shopify.ShopifyResource.activate_session(session1)

        assigned_site = shopify.Session.temp("testshop.myshopify.com", "any-token", "shopify.ShopifyResource.site")
        
        self.assertEqual('https://testshop.myshopify.com/admin', assigned_site)
        self.assertEqual('https://fakeshop.myshopify.com/admin', shopify.ShopifyResource.site)

    def test_create_permission_url_returns_correct_url_with_single_scope_no_redirect_uri(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session('http://localhost.myshopify.com')
        scope = ["write_products"]
        permission_url = session.create_permission_url(scope)
        self.assertEqual("https://localhost.myshopify.com/admin/oauth/authorize?scope=write_products&client_id=My_test_key", permission_url)

    def test_create_permission_url_returns_correct_url_with_single_scope_and_redirect_uri(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session('http://localhost.myshopify.com')
        scope = ["write_products"]
        permission_url = session.create_permission_url(scope, "my_redirect_uri.com")
        self.assertEqual("https://localhost.myshopify.com/admin/oauth/authorize?scope=write_products&redirect_uri=my_redirect_uri.com&client_id=My_test_key", permission_url)
    
    def test_create_permission_url_returns_correct_url_with_dual_scope_no_redirect_uri(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session('http://localhost.myshopify.com')
        scope = ["write_products","write_customers"]
        permission_url = session.create_permission_url(scope)
        self.assertEqual("https://localhost.myshopify.com/admin/oauth/authorize?scope=write_products%2Cwrite_customers&client_id=My_test_key", permission_url)

    def test_create_permission_url_returns_correct_url_with_no_scope_no_redirect_uri(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session('http://localhost.myshopify.com')
        scope = []
        permission_url = session.create_permission_url(scope)
        self.assertEqual("https://localhost.myshopify.com/admin/oauth/authorize?scope=&client_id=My_test_key", permission_url)

    def test_request_token_should_get_token(self):
        shopify.Session.setup(api_key="My test key", secret="My test secret")
        session = shopify.Session('http://localhost.myshopify.com')
        self.fake(None, url='https://localhost.myshopify.com/admin/oauth/access_token', method='POST', body='{"access_token" : "token"}', has_user_agent=False)
        self.assertEqual("token", session.request_token("code"))

    def test_raise_exception_if_code_invalid_in_request_token(self):
        shopify.Session.setup(api_key="My test key", secret="My test secret")
        session = shopify.Session('http://localhost.myshopify.com')
        self.fake(None, url='https://localhost.myshopify.com/admin/oauth/access_token', method='POST', code=404, body='{"error" : "invalid_request"}', has_user_agent=False)
        
        with self.assertRaises(Exception):
            session.request_token("bad_code")

        self.assertFalse(session.valid)

    def test_temp_reset_shopify_ShopifyResource_site_to_original_value_when_using_a_non_standard_port(self):
        shopify.Session.setup(api_key="key", secret="secret")
        session1 = shopify.Session('fakeshop.myshopify.com:3000', 'token1')
        shopify.ShopifyResource.activate_session(session1)

        assigned_site = shopify.Session.temp("testshop.myshopify.com", "any-token", "shopify.ShopifyResource.site")
      
        self.assertEqual('https://testshop.myshopify.com/admin', assigned_site)
        self.assertEqual('https://fakeshop.myshopify.com:3000/admin', shopify.ShopifyResource.site)

    def test_return_site_for_session(self):
        session = shopify.Session("testshop.myshopify.com", "any-token")
        self.assertEqual("https://testshop.myshopify.com/admin", session.site)

    def test_return_session_if_signature_is_valid(self):
        shopify.Session.secret='secret'
        params = {'foo': 'hello', 'timestamp': time.time()}
        sorted_params = self.make_sorted_params(params)
        signature = md5(shopify.Session.secret + sorted_params).hexdigest()
        params['signature'] = signature

        self.fake(None, url='https://localhost.myshopify.com/admin/oauth/access_token', method='POST', body='{"access_token" : "token"}', has_user_agent=False)
        session = shopify.Session('http://localhost.myshopify.com')
        token = session.request_token("code", params=params)
        self.assertTrue(session.valid)

    def test_raise_error_if_signature_does_not_match_expected(self):
        shopify.Session.secret='secret'
        params = {'foo': 'hello', 'timestamp': time.time()}
        sorted_params = self.make_sorted_params(params)
        signature = md5(shopify.Session.secret + sorted_params).hexdigest()
        params['signature'] = signature
        params['bar'] = 'world'

        with self.assertRaises(Exception):
            session = shopify.Session('http://localhost.myshopify.com')
            session = session.request_token("code", params=params)

    def test_raise_error_if_timestamp_is_too_old(self):
        shopify.Session.secret='secret'
        one_day = 24 * 60 * 60
        params = {'foo': 'hello', 'timestamp': time.time()-(2*one_day)}
        sorted_params = self.make_sorted_params(params)
        signature = md5(shopify.Session.secret + sorted_params).hexdigest()
        params['signature'] = signature

        with self.assertRaises(Exception):
            session = shopify.Session('http://localhost.myshopify.com')
            session = session.request_token("code", params=params)


    def make_sorted_params(self, params):
        sorted_params = ""
        for k in sorted(params.keys()):
            if k != "signature":
                sorted_params += k + "=" + str(params[k])
        return sorted_params
