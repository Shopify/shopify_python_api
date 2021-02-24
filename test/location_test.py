import shopify
import json
from test.test_helper import TestCase


class LocationTest(TestCase):
    def test_fetch_locations(self):
        self.fake("locations", method='GET', body=self.load_fixture('locations'))
        locations = shopify.Location.find()
        self.assertEqual(2, len(locations))

    def test_fetch_location(self):
        self.fake("locations/487838322", method='GET', body=self.load_fixture('location'))
        location = shopify.Location.find(487838322)
        self.assertEqual(location.id, 487838322)
        self.assertEqual(location.name, "Fifth Avenue AppleStore")

    def test_inventory_levels_returns_all_inventory_levels(self):
        location = shopify.Location({'id': 487838322})

        self.fake(
            "locations/%s/inventory_levels" % location.id,
            method='GET',
            code=200,
            body=self.load_fixture('location_inventory_levels'),
        )
        inventory_levels = location.inventory_levels()

        self.assertEqual(location.id, inventory_levels[0].location_id)
        self.assertEqual(27, inventory_levels[0].available)
        self.assertEqual(9, inventory_levels[1].available)
