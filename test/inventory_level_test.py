import shopify
import json
from six.moves.urllib.parse import urlencode
from test.test_helper import TestCase


class InventoryLevelTest(TestCase):

    def test_fetch_inventory_level(self):
        params = {'inventory_item_ids': [808950810, 39072856], 'location_ids': [905684977, 487838322]}

        self.fake(
            'inventory_levels.json?location_ids=905684977%2C487838322&inventory_item_ids=808950810%2C39072856',
            method='GET',
            extension='',
            body=self.load_fixture('inventory_levels')
        )
        inventory_levels = shopify.InventoryLevel.find(
            inventory_item_ids='808950810,39072856',
            location_ids='905684977,487838322'
        )
        self.assertTrue(
            all(item.location_id in params['location_ids']
                and item.inventory_item_id in params['inventory_item_ids'] for item in inventory_levels)
        )

    def test_inventory_level_adjust(self):
        self.fake(
            'inventory_levels/adjust',
            method='POST',
            body=self.load_fixture('inventory_level'),
            headers={'Content-type': 'application/json'}
        )
        inventory_level = shopify.InventoryLevel.adjust(905684977, 808950810, 5)
        self.assertEqual(inventory_level.available, 6)

    def test_inventory_level_connect(self):
        self.fake(
            'inventory_levels/connect',
            method='POST',
            body=self.load_fixture('inventory_level'),
            headers={'Content-type': 'application/json'},
            code=201
        )
        inventory_level = shopify.InventoryLevel.connect(905684977, 808950810)
        self.assertEqual(inventory_level.available, 6)

    def test_inventory_level_set(self):
        self.fake(
            'inventory_levels/set',
            method='POST',
            body=self.load_fixture('inventory_level'),
            headers={'Content-type': 'application/json'},
        )
        inventory_level = shopify.InventoryLevel.set(905684977, 808950810, 6)
        self.assertEqual(inventory_level.available, 6)

    def test_destroy_inventory_level(self):
        inventory_level_response = json.loads(self.load_fixture('inventory_level').decode())
        inventory_level = shopify.InventoryLevel(inventory_level_response['inventory_level'])

        query_params = urlencode({
            'inventory_item_id': inventory_level.inventory_item_id,
            'location_id': inventory_level.location_id
        })
        path = "inventory_levels.json?" + query_params

        self.fake(path, extension=False, method='DELETE', code=204, body='{}')
        inventory_level.destroy()
