import shopify
import json
from test.test_helper import TestCase


class PaginationTest(TestCase):

    def setUp(self):
        super(PaginationTest, self).setUp()
        prefix = self.http.site + "/admin/api/unstable"
        fixture = json.loads(self.load_fixture('products').decode())

        self.next_page_url = prefix + "/products.json?limit=2&page_info=FOOBAR"
        self.prev_page_url = prefix + "/products.json?limit=2&page_info=BAZQUUX"

        next_headers = {"Link": "<" + self.next_page_url + ">; rel=\"next\""}
        prev_headers = {"Link": "<" + self.prev_page_url + ">; rel=\"previous\""}

        self.fake("products",
                  url=prefix + "/products.json?limit=2",
                  body=json.dumps({"products": fixture[:2]}),
                  response_headers=next_headers)
        self.fake("products",
                  url=prefix + "/products.json?limit=2&page_info=FOOBAR",
                  body=json.dumps({"products": fixture[2:4]}),
                  response_headers=prev_headers)
        self.fake("products",
                  url=prefix + "/products.json?limit=2&page_info=BAZQUUX",
                  body=json.dumps({"products": fixture[:2]}),
                  response_headers=next_headers)

    def test_nonpaginates_collection(self):
        self.fake('draft_orders', method='GET', code=200, body=self.load_fixture('draft_orders'))
        draft_orders = shopify.DraftOrder.find()
        self.assertEqual(1, len(draft_orders))
        self.assertEqual(517119332, draft_orders[0].id)
        self.assertIsInstance(draft_orders, shopify.collection.PaginatedCollection,
                              "find() result is not PaginatedCollection")

    def test_paginated_collection(self):
        items = shopify.Product.find(limit=2)
        self.assertIsInstance(items, shopify.collection.PaginatedCollection, "find() result is not PaginatedCollection")
        self.assertEqual(len(items), 2, "find() result has incorrect length")

    def test_pagination_next_page(self):
        c = shopify.Product.find(limit=2)
        self.assertEqual(c.next_page_url, self.next_page_url, "next url is incorrect")
        n = c.next_page()
        self.assertEqual(n.previous_page_url, self.prev_page_url, "prev url is incorrect")
        self.assertIsInstance(n, shopify.collection.PaginatedCollection,
                              "next_page() result is not PaginatedCollection")
        self.assertEqual(len(n), 2, "next_page() collection has incorrect length")
        self.assertIn("pagination", n.metadata)
        self.assertIn("previous", n.metadata["pagination"],
                      "next_page() collection doesn't have a previous page")

        with self.assertRaises(IndexError, msg="next_page() did not raise with no next page"):
            n.next_page()

    def test_pagination_previous(self):
        c = shopify.Product.find(limit=2)
        self.assertEqual(c.next_page_url, self.next_page_url, "next url is incorrect")
        self.assertTrue(c.has_next_page())
        n = c.next_page()
        self.assertEqual(n.previous_page_url, self.prev_page_url, "prev url is incorrect")
        self.assertTrue(n.has_previous_page())

        p = n.previous_page()

        self.assertIsInstance(p, shopify.collection.PaginatedCollection,
                              "previous_page() result is not PaginatedCollection")
        self.assertEqual(len(p), 4,  # cached
                         "previous_page() collection has incorrect length")
        self.assertIn("pagination", p.metadata)
        self.assertIn("next", p.metadata["pagination"],
                      "previous_page() collection doesn't have a next page")

        with self.assertRaises(IndexError, msg="previous_page() did not raise with no previous page"):
            p.previous_page()

    def test_paginated_collection_iterator(self):
        c = shopify.Product.find(limit=2)

        i = iter(c)
        self.assertEqual(next(i).id, 1)
        self.assertEqual(next(i).id, 2)
        with self.assertRaises(StopIteration):
            next(i)

    def test_paginated_collection_no_cache(self):
        c = shopify.Product.find(limit=2)

        n = c.next_page(no_cache=True)
        self.assertIsNone(c._next, "no_cache=True still caches")
        self.assertIsNone(n._previous, "no_cache=True still caches")

        p = n.previous_page(no_cache=True)
        self.assertIsNone(p._next, "no_cache=True still caches")
        self.assertIsNone(n._previous, "no_cache=True still caches")

    def test_paginated_iterator(self):
        c = shopify.Product.find(limit=2)

        i = iter(shopify.PaginatedIterator(c))

        first_page = iter(next(i))
        self.assertEqual(next(first_page).id, 1)
        self.assertEqual(next(first_page).id, 2)
        with self.assertRaises(StopIteration):
            next(first_page)

        second_page = iter(next(i))
        self.assertEqual(next(second_page).id, 3)
        self.assertEqual(next(second_page).id, 4)
        with self.assertRaises(StopIteration):
            next(second_page)

        with self.assertRaises(StopIteration):
            next(i)
