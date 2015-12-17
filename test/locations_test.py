import shopify
from test.test_helper import TestCase

class LocationsTest(TestCase):
    def test_fetch_locations(self):
        self.fake("locations", method='GET', body=self.load_fixture('locations'))
        locations = shopify.Location.find()
        self.assertEqual(2,len(locations))

    def test_fetch_location(self):
        self.fake("locations/487838322", method='GET', body=self.load_fixture('location'))
        location = shopify.Location.find(487838322)
        self.assertEqual(location.id,487838322)
        self.assertEqual(location.name,"Fifth Avenue AppleStore")
