import shopify
from test.test_helper import TestCase


class ApiVersionTest(TestCase):
    """
    Api Version Tests
    """

    def tearDown(self):
        shopify.ApiVersion.clear_defined_versions()
        shopify.ApiVersion.define_known_versions()

    def test_unstable_api_path_returns_correct_url(self):
        self.assertEqual(
            "https://fakeshop.myshopify.com/admin/api/unstable",
            shopify.Unstable().api_path("https://fakeshop.myshopify.com"),
        )

    def test_coerce_to_version_returns_known_versions(self):
        v1 = shopify.Unstable()
        v2 = shopify.ApiVersion.define_version(shopify.Release("2019-01"))

        self.assertNotEqual(v1, None)
        self.assertEqual(v1, shopify.ApiVersion.coerce_to_version("unstable"))
        self.assertEqual(v2, shopify.ApiVersion.coerce_to_version("2019-01"))

    def test_coerce_to_version_raises_with_string_that_does_not_match_known_version(self):
        with self.assertRaises(shopify.VersionNotFoundError):
            shopify.ApiVersion.coerce_to_version("crazy-name")


class ReleaseTest(TestCase):
    def test_raises_if_format_invalid(self):
        with self.assertRaises(shopify.InvalidVersionError):
            shopify.Release("crazy-name")

    def test_release_api_path_returns_correct_url(self):
        self.assertEqual(
            "https://fakeshop.myshopify.com/admin/api/2019-04",
            shopify.Release("2019-04").api_path("https://fakeshop.myshopify.com"),
        )

    def test_two_release_versions_with_same_number_are_equal(self):
        version1 = shopify.Release("2019-01")
        version2 = shopify.Release("2019-01")
        self.assertEqual(version1, version2)
