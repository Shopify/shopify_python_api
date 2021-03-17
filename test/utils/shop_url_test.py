from shopify.utils import shop_url
from test.test_helper import TestCase


class TestSanitizeShopDomain(TestCase):
    def test_returns_hostname_for_good_shop_domains(self):
        good_shop_domains = [
            "my-shop",
            "my-shop.myshopify.com",
            "http://my-shop.myshopify.com",
            "https://my-shop.myshopify.com",
        ]
        sanitized_shops = [shop_url.sanitize_shop_domain(shop_domain) for shop_domain in good_shop_domains]

        self.assertTrue(all(shop == "my-shop.myshopify.com" for shop in sanitized_shops))

    def test_returns_none_for_bad_shop_domains(self):
        bad_shop_domains = [
            "myshop.com",
            "myshopify.com",
            "shopify.com",
            "two words",
            "store.myshopify.com.evil.com",
            "/foo/bar",
            "/foo.myshopify.io.evil.ru",
            "%0a123.myshopify.io ",
            "foo.bar.myshopify.io",
        ]
        sanitized_shops = [shop_url.sanitize_shop_domain(shop_domain) for shop_domain in bad_shop_domains]

        self.assertTrue(all(shop_domain is None for shop_domain in sanitized_shops))

    def test_returns_hostname_for_custom_shop_domains(self):
        custom_shop_domains = [
            "my-shop",
            "my-shop.myshopify.io",
            "http://my-shop.myshopify.io",
            "https://my-shop.myshopify.io",
        ]
        sanitized_shops = [
            shop_url.sanitize_shop_domain(shop_domain, "myshopify.io") for shop_domain in custom_shop_domains
        ]

        self.assertTrue(all(shop == "my-shop.myshopify.io" for shop in sanitized_shops))
