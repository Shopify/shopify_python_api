import shopify
from test.test_helper import TestCase

class CollectionListingTest(TestCase):

    def test_get_collection_listings(self):
        self.fake('collection_listings', method='GET', status=200, body=self.load_fixture('collection_listings'))

        collection_listings = shopify.CollectionListing.find()
        self.assertEqual(1, len(collection_listings))
        self.assertEqual(1, collection_listings[0].collection_id)
        self.assertEqual("Home page", collection_listings[0].title)

    def test_get_collection_listing(self):
        self.fake('collection_listings/1', method='GET', status=200, body=self.load_fixture('collection_listing'))

        collection_listing = shopify.CollectionListing.find(1)

        self.assertEqual(1, collection_listing.collection_id)
        self.assertEqual("Home page", collection_listing.title)

    def test_reload_collection_listing(self):
        self.fake('collection_listings/1', method='GET', status=200, body=self.load_fixture('collection_listing'))

        collection_listing = shopify.CollectionListing()
        collection_listing.collection_id = 1
        collection_listing.reload()

        self.assertEqual(1, collection_listing.collection_id)
        self.assertEqual("Home page", collection_listing.title)

    def test_get_collection_listing_product_ids(self):
        self.fake('collection_listings/1/product_ids', method='GET', status=200, body=self.load_fixture('collection_listing_product_ids'))

        collection_listing = shopify.CollectionListing()
        collection_listing.id = 1
        product_ids = collection_listing.product_ids()

        self.assertEqual([1, 2], product_ids)
