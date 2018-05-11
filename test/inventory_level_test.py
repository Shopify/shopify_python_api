import shopify
from test.test_helper import TestCase


class InventoryLevelTest(TestCase):

    def test_fetch_inventory_level(self):
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
        self.assertEqual(4, len(inventory_levels))

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
