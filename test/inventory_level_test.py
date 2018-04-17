import json
import shopify
import urllib
from test.test_helper import TestCase


class InventoryLevelTest(TestCase):

    def setUp(self):
        super(InventoryLevelTest, self).setUp()

        self.inventory_level_response = json.loads(self.load_fixture('inventory_level'))
        self.inventory_level = shopify.InventoryLevel(self.inventory_level_response['inventory_level'])

    def test_find_with_inventory_item_ids_and_location_ids(self):
        params = {'inventory_item_ids': [808950810, 39072856], 'location_ids': [905684977, 487838322]}
        self.fake("inventory_levels.json?%s" % urllib.urlencode(params, True), extension=False, method='GET', status=200, body=self.load_fixture('inventory_levels'))
        inventory_levels = shopify.InventoryLevel.find(params) # TODO: this is failing

        # TODO: assert membership of inventory_levels

        self.assertTrue(False)