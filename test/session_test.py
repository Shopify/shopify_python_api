import shopify
from test.test_helper import TestCase
import hmac
from hashlib import sha256
import time
from six.moves import urllib
from six import u


class SessionTest(TestCase):
    @classmethod
    def setUpClass(self):
        shopify.ApiVersion.define_known_versions()
        shopify.ApiVersion.define_version(shopify.Release("2019-04"))

    @classmethod
    def tearDownClass(self):
        shopify.ApiVersion.clear_defined_versions()

    def test_not_be_valid_without_a_url(self):
        session = shopify.Session("", "unstable", "any-token")
        self.assertFalse(session.valid)

    def test_not_be_valid_without_token(self):
        session = shopify.Session("testshop.myshopify.com", "unstable")
        self.assertFalse(session.valid)

    def test_be_valid_with_any_token_and_any_url(self):
        session = shopify.Session("testshop.myshopify.com", "unstable", "any-token")
        self.assertTrue(session.valid)

    def test_ignore_everything_but_the_subdomain_in_the_shop(self):
        session = shopify.Session("http://user:pass@testshop.notshopify.net/path", "unstable", "any-token")
        self.assertEqual("https://testshop.myshopify.com/admin/api/unstable", session.site)

    def test_append_the_myshopify_domain_if_not_given(self):
        session = shopify.Session("testshop", "unstable", "any-token")
        self.assertEqual("https://testshop.myshopify.com/admin/api/unstable", session.site)

    def test_raise_error_if_params_passed_but_signature_omitted(self):
        with self.assertRaises(shopify.ValidationException):
            session = shopify.Session("testshop.myshopify.com", "unstable")
            token = session.request_token({"code": "any_code", "foo": "bar", "timestamp": "1234"})

    def test_setup_api_key_and_secret_for_all_sessions(self):
        shopify.Session.setup(api_key="My test key", secret="My test secret")
        self.assertEqual("My test key", shopify.Session.api_key)
        self.assertEqual("My test secret", shopify.Session.secret)

    def test_use_https_protocol_by_default_for_all_sessions(self):
        self.assertEqual("https", shopify.Session.protocol)

    def test_temp_reset_shopify_shopify_resource_site_to_original_value(self):
        shopify.Session.setup(api_key="key", secret="secret")
        session1 = shopify.Session("fakeshop.myshopify.com", "2019-04", "token1")
        shopify.ShopifyResource.activate_session(session1)

        assigned_site = ""
        with shopify.Session.temp("testshop.myshopify.com", "unstable", "any-token"):
            assigned_site = shopify.ShopifyResource.site

        self.assertEqual("https://testshop.myshopify.com/admin/api/unstable", assigned_site)
        self.assertEqual("https://fakeshop.myshopify.com/admin/api/2019-04", shopify.ShopifyResource.site)

    def test_myshopify_domain_supports_non_standard_ports(self):
        try:
            shopify.Session.setup(api_key="key", secret="secret", myshopify_domain="localhost", port=3000)

            session = shopify.Session("fakeshop.localhost:3000", "unstable", "token1")
            shopify.ShopifyResource.activate_session(session)
            self.assertEqual("https://fakeshop.localhost:3000/admin/api/unstable", shopify.ShopifyResource.site)

            session = shopify.Session("fakeshop", "unstable", "token1")
            shopify.ShopifyResource.activate_session(session)
            self.assertEqual("https://fakeshop.localhost:3000/admin/api/unstable", shopify.ShopifyResource.site)
        finally:
            shopify.Session.setup(myshopify_domain="myshopify.com", port=None)

    def test_temp_works_without_currently_active_session(self):
        shopify.ShopifyResource.clear_session()

        assigned_site = ""
        with shopify.Session.temp("testshop.myshopify.com", "unstable", "any-token"):
            assigned_site = shopify.ShopifyResource.site

        self.assertEqual("https://testshop.myshopify.com/admin/api/unstable", assigned_site)
        self.assertEqual("https://none/admin/api/unstable", shopify.ShopifyResource.site)

    def test_create_permission_url_returns_correct_url_with_redirect_uri(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session("http://localhost.myshopify.com", "unstable")
        permission_url = session.create_permission_url("my_redirect_uri.com")
        self.assertEqual(
            "https://localhost.myshopify.com/admin/oauth/authorize?client_id=My_test_key&redirect_uri=my_redirect_uri.com",
            self.normalize_url(permission_url),
        )

    def test_create_permission_url_returns_correct_url_with_redirect_uri_and_single_scope(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session("http://localhost.myshopify.com", "unstable")
        scope = ["write_products"]
        permission_url = session.create_permission_url("my_redirect_uri.com", scope=scope)
        self.assertEqual(
            "https://localhost.myshopify.com/admin/oauth/authorize?client_id=My_test_key&redirect_uri=my_redirect_uri.com&scope=write_products",
            self.normalize_url(permission_url),
        )

    def test_create_permission_url_returns_correct_url_with_redirect_uri_and_dual_scope(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session("http://localhost.myshopify.com", "unstable")
        scope = ["write_products", "write_customers"]
        permission_url = session.create_permission_url("my_redirect_uri.com", scope=scope)
        self.assertEqual(
            "https://localhost.myshopify.com/admin/oauth/authorize?client_id=My_test_key&redirect_uri=my_redirect_uri.com&scope=write_products%2Cwrite_customers",
            self.normalize_url(permission_url),
        )

    def test_create_permission_url_returns_correct_url_with_redirect_uri_and_empty_scope(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session("http://localhost.myshopify.com", "unstable")
        scope = []
        permission_url = session.create_permission_url("my_redirect_uri.com", scope=scope)
        self.assertEqual(
            "https://localhost.myshopify.com/admin/oauth/authorize?client_id=My_test_key&redirect_uri=my_redirect_uri.com",
            self.normalize_url(permission_url),
        )

    def test_create_permission_url_returns_correct_url_with_redirect_uri_and_state(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session("http://localhost.myshopify.com", "unstable")
        permission_url = session.create_permission_url("my_redirect_uri.com", state="mystate")
        self.assertEqual(
            "https://localhost.myshopify.com/admin/oauth/authorize?client_id=My_test_key&redirect_uri=my_redirect_uri.com&state=mystate",
            self.normalize_url(permission_url),
        )

    def test_create_permission_url_returns_correct_url_with_redirect_uri_empty_scope_and_state(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session("http://localhost.myshopify.com", "unstable")
        scope = []
        permission_url = session.create_permission_url("my_redirect_uri.com", scope=scope, state="mystate")
        self.assertEqual(
            "https://localhost.myshopify.com/admin/oauth/authorize?client_id=My_test_key&redirect_uri=my_redirect_uri.com&state=mystate",
            self.normalize_url(permission_url),
        )

    def test_create_permission_url_returns_correct_url_with_redirect_uri_and_single_scope_and_state(self):
        shopify.Session.setup(api_key="My_test_key", secret="My test secret")
        session = shopify.Session("http://localhost.myshopify.com", "unstable")
        scope = ["write_customers"]
        permission_url = session.create_permission_url("my_redirect_uri.com", scope=scope, state="mystate")
        self.assertEqual(
            "https://localhost.myshopify.com/admin/oauth/authorize?client_id=My_test_key&redirect_uri=my_redirect_uri.com&scope=write_customers&state=mystate",
            self.normalize_url(permission_url),
        )

    def test_raise_exception_if_code_invalid_in_request_token(self):
        shopify.Session.setup(api_key="My test key", secret="My test secret")
        session = shopify.Session("http://localhost.myshopify.com", "unstable")
        self.fake(
            None,
            url="https://localhost.myshopify.com/admin/oauth/access_token",
            method="POST",
            code=404,
            body='{"error" : "invalid_request"}',
            has_user_agent=False,
        )

        with self.assertRaises(shopify.ValidationException):
            session.request_token({"code": "any-code", "timestamp": "1234"})

        self.assertFalse(session.valid)

    def test_return_site_for_session(self):
        session = shopify.Session("testshop.myshopify.com", "unstable", "any-token")
        self.assertEqual("https://testshop.myshopify.com/admin/api/unstable", session.site)

    def test_hmac_calculation(self):
        # Test using the secret and parameter examples given in the Shopify API documentation.
        shopify.Session.secret = "hush"
        params = {
            "shop": "some-shop.myshopify.com",
            "code": "a94a110d86d2452eb3e2af4cfb8a3828",
            "timestamp": "1337178173",
            "hmac": "2cb1a277650a659f1b11e92a4a64275b128e037f2c3390e3c8fd2d8721dac9e2",
        }
        self.assertEqual(shopify.Session.calculate_hmac(params), params["hmac"])

    def test_hmac_calculation_with_ampersand_and_equal_sign_characters(self):
        shopify.Session.secret = "secret"
        params = {"a": "1&b=2", "c=3&d": "4"}
        to_sign = "a=1%26b=2&c%3D3%26d=4"
        expected_hmac = hmac.new("secret".encode(), to_sign.encode(), sha256).hexdigest()
        self.assertEqual(shopify.Session.calculate_hmac(params), expected_hmac)

    def test_hmac_validation(self):
        # Test using the secret and parameter examples given in the Shopify API documentation.
        shopify.Session.secret = "hush"
        params = {
            "shop": "some-shop.myshopify.com",
            "code": "a94a110d86d2452eb3e2af4cfb8a3828",
            "timestamp": "1337178173",
            "hmac": u("2cb1a277650a659f1b11e92a4a64275b128e037f2c3390e3c8fd2d8721dac9e2"),
        }
        self.assertTrue(shopify.Session.validate_hmac(params))

    def test_parameter_validation_handles_missing_params(self):
        # Test using the secret and parameter examples given in the Shopify API documentation.
        shopify.Session.secret = "hush"
        params = {
            "shop": "some-shop.myshopify.com",
            "code": "a94a110d86d2452eb3e2af4cfb8a3828",
            "hmac": u("2cb1a277650a659f1b11e92a4a64275b128e037f2c3390e3c8fd2d8721dac9e2"),
        }
        self.assertFalse(shopify.Session.validate_params(params))

    def test_param_validation_of_param_values_with_lists(self):
        shopify.Session.secret = "hush"
        params = {
            "shop": "some-shop.myshopify.com",
            "ids[]": [
                2,
                1,
            ],
            "hmac": u("b93b9f82996f6f8bf9f1b7bbddec284c8fabacdc4e12dc80550b4705f3003b1e"),
        }
        self.assertEqual(True, shopify.Session.validate_hmac(params))

    def test_return_token_and_scope_if_hmac_is_valid(self):
        shopify.Session.secret = "secret"
        params = {"code": "any-code", "timestamp": time.time()}
        hmac = shopify.Session.calculate_hmac(params)
        params["hmac"] = hmac

        self.fake(
            None,
            url="https://localhost.myshopify.com/admin/oauth/access_token",
            method="POST",
            body='{"access_token" : "token", "scope": "read_products,write_orders"}',
            has_user_agent=False,
        )
        session = shopify.Session("http://localhost.myshopify.com", "unstable")
        token = session.request_token(params)
        self.assertEqual("token", token)
        self.assertEqual(shopify.ApiAccess("read_products,write_orders"), session.access_scopes)

    def test_raise_error_if_hmac_is_invalid(self):
        shopify.Session.secret = "secret"
        params = {"code": "any-code", "timestamp": time.time()}
        params["hmac"] = "a94a110d86d2452e92a4a64275b128e9273be3037f2c339eb3e2af4cfb8a3828"

        with self.assertRaises(shopify.ValidationException):
            session = shopify.Session("http://localhost.myshopify.com", "unstable")
            session = session.request_token(params)

    def test_raise_error_if_hmac_does_not_match_expected(self):
        shopify.Session.secret = "secret"
        params = {"foo": "hello", "timestamp": time.time()}
        hmac = shopify.Session.calculate_hmac(params)
        params["hmac"] = hmac
        params["bar"] = "world"
        params["code"] = "code"

        with self.assertRaises(shopify.ValidationException):
            session = shopify.Session("http://localhost.myshopify.com", "unstable")
            session = session.request_token(params)

    def test_raise_error_if_timestamp_is_too_old(self):
        shopify.Session.secret = "secret"
        one_day = 24 * 60 * 60
        params = {"code": "any-code", "timestamp": time.time() - (2 * one_day)}
        hmac = shopify.Session.calculate_hmac(params)
        params["hmac"] = hmac

        with self.assertRaises(shopify.ValidationException):
            session = shopify.Session("http://localhost.myshopify.com", "unstable")
            session = session.request_token(params)

    def test_access_scopes_are_nil_by_default(self):
        session = shopify.Session("testshop.myshopify.com", "unstable", "any-token")
        self.assertIsNone(session.access_scopes)

    def test_access_scopes_when_valid_scopes_passed_in(self):
        session = shopify.Session(
            shop_url="testshop.myshopify.com",
            version="unstable",
            token="any-token",
            access_scopes="read_products, write_orders",
        )

        expected_access_scopes = shopify.ApiAccess("read_products, write_orders")
        self.assertEqual(expected_access_scopes, session.access_scopes)

    def test_access_scopes_set_with_api_access_object_passed_in(self):
        session = shopify.Session(
            shop_url="testshop.myshopify.com",
            version="unstable",
            token="any-token",
            access_scopes=shopify.ApiAccess("read_products, write_orders"),
        )

        expected_access_scopes = shopify.ApiAccess("read_products, write_orders")
        self.assertEqual(expected_access_scopes, session.access_scopes)

    def normalize_url(self, url):
        scheme, netloc, path, query, fragment = urllib.parse.urlsplit(url)
        query = "&".join(sorted(query.split("&")))
        return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))

    def test_session_with_coerced_version(self):
        future_version = "2030-01"
        session = shopify.Session("test.myshopify.com", future_version, "token")
        self.assertEqual(session.api_version.name, future_version)
        self.assertEqual(
            session.api_version.api_path("https://test.myshopify.com"),
            f"https://test.myshopify.com/admin/api/{future_version}",
        )

    def test_session_with_invalid_version(self):
        with self.assertRaises(shopify.VersionNotFoundError):
            shopify.Session("test.myshopify.com", "invalid-version", "token")
