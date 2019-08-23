import shopify
import json
from test.test_helper import TestCase

class CollectionTest(TestCase):

    def setUp(self):
        super(CollectionTest, self).setUp()

        fixture = json.loads(self.load_fixture('products'))

        # Assumes limit is 2
        prefix = self.http.site + "/admin/api/unstable"

        next_headers = {
            "Link": "<" + prefix + "/products.json?limit=2&page_info="
            "FOOBAR>; rel=\"next\""
        }
        next_body = json.dumps({ "products": fixture[:2] })

        self.fake("products",
                  url=prefix + "/products.json",
                  body=next_body,
                  response_headers=next_headers)
        self.fake("products",
                  url=prefix + "/products.json?limit=2&page_info=BAZQUUX",
                  body=next_body,
                  response_headers=next_headers)
        self.fake("products",
                  url=prefix + "/products.json?limit=2&page_info=FOOBAR",
                  body=json.dumps({ "products": fixture[2:] }),
                  response_headers={
                      "Link": "<" + prefix + "/products.json?limit=2&page_info="
                      "BAZQUUX>; rel=\"previous\""
                  })


    def test_paginated_collection(self):
        items = shopify.Product.find()

        self.assertIsInstance(items, shopify.collection.PaginatedCollection,
                              "find() result is not PaginatedCollection")
        self.assertEqual(len(items), 2,
                         "find() result has incorrect length")

    def test_pagination_next(self):
        c = shopify.Product.find()

        n = c.next()
        self.assertIsInstance(n, shopify.collection.PaginatedCollection,
                              "next() result is not PaginatedCollection")
        self.assertEqual(len(n), 2,
                         "next() collection has incorrect length")
        self.assertIn("pagination", n.metadata)
        self.assertIn("previous", n.metadata["pagination"],
                      "next() collection doesn't have a previous page")

        with self.assertRaises(IndexError, msg="next() did not raise with no next page"):
            n.next()

    def test_pagination_previous(self):
        c = shopify.Product.find()
        n = c.next()

        p = n.previous()

        self.assertIsInstance(p, shopify.collection.PaginatedCollection,
                              "previous() result is not PaginatedCollection")
        self.assertEqual(len(p), 4, # cached
                         "previous() collection has incorrect length")
        self.assertIn("pagination", p.metadata)
        self.assertIn("next", p.metadata["pagination"],
                      "previous() collection doesn't have a next page")

        with self.assertRaises(IndexError, msg="previous() did not raise with no previous page"):
            p.previous()

    def test_paginated_collection_iterator(self):
        c = shopify.Product.find()

        i = iter(c)
        self.assertEqual(next(i).id, 1)
        self.assertEqual(next(i).id, 2)
        self.assertEqual(next(i).id, 3)
        self.assertEqual(next(i).id, 4)
        with self.assertRaises(StopIteration):
            next(i)

    def test_paginated_collection_no_cache(self):
        c = shopify.Product.find()

        n = c.next(no_cache=True)
        self.assertIsNone(c._next, "no_cache=True still caches")
        self.assertIsNone(n._previous, "no_cache=True still caches")

        p = n.previous(no_cache=True)
        self.assertIsNone(p._next, "no_cache=True still caches")
        self.assertIsNone(n._previous, "no_cache=True still caches")

    def test_paginated_iterator(self):
        c = shopify.Product.find()

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
