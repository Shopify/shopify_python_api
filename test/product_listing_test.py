import shopify
from test.test_helper import TestCase

class ProductListingTest(TestCase):

    def test_get_product_listings(self):
        self.fake('product_listings', method='GET', status=200, body=self.load_fixture('product_listings'))

        product_listings = shopify.ProductListing.find()
        self.assertEqual(2, len(product_listings))
        self.assertEqual(2, product_listings[0].product_id)
        self.assertEqual(1, product_listings[1].product_id)
        self.assertEqual("Synergistic Silk Chair", product_listings[0].title)
        self.assertEqual("Rustic Copper Bottle", product_listings[1].title)

    def test_get_product_listing(self):
        self.fake('product_listings/2', method='GET', status=200, body=self.load_fixture('product_listing'))

        product_listing = shopify.ProductListing.find(2)
        self.assertEqual("Synergistic Silk Chair", product_listing.title)

    def test_reload_product_listing(self):
        self.fake('product_listings/2', method='GET', status=200, body=self.load_fixture('product_listing'))

        product_listing = shopify.ProductListing()
        product_listing.product_id = 2
        product_listing.reload()

        self.assertEqual("Synergistic Silk Chair", product_listing.title)

    def test_get_product_listing_product_ids(self):
        self.fake('product_listings/product_ids', method='GET', status = 200, body=self.load_fixture('product_listing_product_ids'))

        product_ids = shopify.ProductListing.product_ids()

        self.assertEqual(2, len(product_ids))
        self.assertEqual(2, product_ids[0])
        self.assertEqual(1, product_ids[1])
