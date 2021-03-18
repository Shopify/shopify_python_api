from shopify import ApiAccess, ApiAccessError
from test.test_helper import TestCase


class ApiAccessTest(TestCase):
    def test_creating_scopes_from_a_string_works_with_a_comma_separated_list(self):
        deserialized_read_products_write_orders = ApiAccess("read_products,write_orders")
        serialized_read_products_write_orders = str(deserialized_read_products_write_orders)
        expected_read_products_write_orders = ApiAccess(["read_products", "write_orders"])

        self.assertEqual(expected_read_products_write_orders, ApiAccess(serialized_read_products_write_orders))

    def test_creating_api_access_from_invalid_scopes_raises(self):
        with self.assertRaises(ApiAccessError) as cm:
            api_access = ApiAccess("bad_scope, read_orders,write_orders")

        self.assertEqual("'bad_scope' is not a valid access scope", str(cm.exception))

    def test_returns_list_of_reduced_scopes(self):
        api_access = ApiAccess("read_products, read_orders,write_orders")
        expected_scopes = set(["read_products", "write_orders"])
        scopes = list(api_access)

        self.assertEqual(expected_scopes, set(scopes))

    def test_write_is_the_same_access_as_read_write_on_the_same_resource(self):
        read_write_orders = ApiAccess(["read_orders", "write_orders"])
        write_orders = ApiAccess("write_orders")

        self.assertEqual(write_orders, read_write_orders)

    def test_write_is_the_same_access_as_read_write_on_the_same_unauthenticated_resource(self):
        unauthenticated_read_write_orders = ApiAccess(["unauthenticated_read_orders", "unauthenticated_write_orders"])
        unauthenticated_write_orders = ApiAccess("unauthenticated_write_orders")

        self.assertEqual(unauthenticated_write_orders, unauthenticated_read_write_orders)

    def test_read_is_not_the_same_as_read_write_on_the_same_resource(self):
        read_orders = ApiAccess("read_orders")
        read_write_orders = ApiAccess(["write_orders", "read_orders"])

        self.assertNotEqual(read_write_orders, read_orders)

    def test_two_different_resources_are_not_equal(self):
        read_orders = ApiAccess("read_orders")
        read_products = ApiAccess("read_products")

        self.assertNotEqual(read_orders, read_products)

    def test_two_identical_scopes_are_equal(self):
        read_orders = ApiAccess("read_orders")
        read_orders_identical = ApiAccess("read_orders")

        self.assertEqual(read_orders, read_orders_identical)

    def test_unauthenticated_is_not_implied_by_authenticated_access(self):
        unauthenticated_orders = ApiAccess("unauthenticated_read_orders")
        authenticated_read_orders = ApiAccess("read_orders")
        authenticated_write_orders = ApiAccess("write_orders")

        self.assertNotEqual(unauthenticated_orders, authenticated_read_orders)
        self.assertNotEqual(unauthenticated_orders, authenticated_write_orders)

    def test_scopes_covers_is_truthy_for_same_scopes(self):
        read_orders = ApiAccess("read_orders")
        read_orders_identical = ApiAccess("read_orders")

        self.assertTrue(read_orders.covers(read_orders_identical))

    def test_covers_is_falsy_for_different_scopes(self):
        read_orders = ApiAccess("read_orders")
        read_products = ApiAccess("read_products")

        self.assertFalse(read_orders.covers(read_products))

    def test_covers_is_truthy_for_read_when_the_set_has_read_write(self):
        write_products = ApiAccess("write_products")
        read_products = ApiAccess("read_products")

        self.assertTrue(write_products.covers(read_products))

    def test_covers_is_truthy_for_read_when_the_set_has_read_write_for_that_resource_and_others(self):
        write_products_and_orders = ApiAccess(["write_products", "write_orders"])
        read_orders = ApiAccess("read_orders")

        self.assertTrue(write_products_and_orders.covers(read_orders))

    def test_covers_is_truthy_for_write_when_the_set_has_read_write_for_that_resource_and_others(self):
        write_products_and_orders = ApiAccess(["write_products", "write_orders"])
        write_orders = ApiAccess("write_orders")

        self.assertTrue(write_products_and_orders.covers(write_orders))

    def test_covers_is_truthy_for_subset_of_scopes(self):
        write_products_orders_customers = ApiAccess(["write_products", "write_orders", "write_customers"])
        write_orders_products = ApiAccess(["write_orders", "read_products"])

        self.assertTrue(write_products_orders_customers.covers(write_orders_products))

    def test_covers_is_falsy_for_sets_of_scopes_that_have_no_common_elements(self):
        write_products_orders_customers = ApiAccess(["write_products", "write_orders", "write_customers"])
        write_images_read_content = ApiAccess(["write_images", "read_content"])

        self.assertFalse(write_products_orders_customers.covers(write_images_read_content))

    def test_covers_is_falsy_for_sets_of_scopes_that_have_only_some_common_access(self):
        write_products_orders_customers = ApiAccess(["write_products", "write_orders", "write_customers"])
        write_products_read_content = ApiAccess(["write_products", "read_content"])

        self.assertFalse(write_products_orders_customers.covers(write_products_read_content))

    def test_duplicate_scopes_resolve_to_one_scope(self):
        read_orders_duplicated = ApiAccess(["read_orders", "read_orders", "read_orders", "read_orders"])
        read_orders = ApiAccess("read_orders")

        self.assertEqual(read_orders, read_orders_duplicated)

    def test_to_s_outputs_scopes_as_a_comma_separated_list_without_implied_read_scopes(self):
        serialized_read_products_write_orders = "read_products,write_orders"
        read_products_write_orders = ApiAccess(["read_products", "read_orders", "write_orders"])

        self.assertIn("read_products", str(read_products_write_orders))
        self.assertIn("write_orders", str(read_products_write_orders))

    def test_to_a_outputs_scopes_as_an_array_of_strings_without_implied_read_scopes(self):
        serialized_read_products_write_orders = ["write_orders", "read_products"]
        read_products_write_orders = ApiAccess(["read_products", "read_orders", "write_orders"])

        self.assertEqual(set(serialized_read_products_write_orders), set(list(read_products_write_orders)))

    def test_creating_scopes_removes_extra_whitespace_from_scope_name_and_blank_scope_names(self):
        deserialized_read_products_write_orders = ApiAccess([" read_products", "  ", "write_orders "])
        serialized_read_products_write_orders = str(deserialized_read_products_write_orders)
        expected_read_products_write_orders = ApiAccess(["read_products", "write_orders"])

        self.assertEqual(expected_read_products_write_orders, ApiAccess(serialized_read_products_write_orders))

    def test_creating_scopes_from_a_string_works_with_a_comma_separated_list(self):
        deserialized_read_products_write_orders = ApiAccess("read_products,write_orders")
        serialized_read_products_write_orders = str(deserialized_read_products_write_orders)
        expected_read_products_write_orders = ApiAccess(["read_products", "write_orders"])

        self.assertEqual(expected_read_products_write_orders, ApiAccess(serialized_read_products_write_orders))

    def test_using_to_s_from_one_scopes_to_construct_another_will_be_equal(self):
        read_products_write_orders = ApiAccess(["read_products", "write_orders"])

        self.assertEqual(read_products_write_orders, ApiAccess(str(read_products_write_orders)))

    def test_using_to_a_from_one_scopes_to_construct_another_will_be_equal(self):
        read_products_write_orders = ApiAccess(["read_products", "write_orders"])

        self.assertEqual(read_products_write_orders, ApiAccess(list(read_products_write_orders)))
