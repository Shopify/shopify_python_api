import shopify
from test.test_helper import TestCase


class InventoryItemTest(TestCase):
    def test_fetch_inventory_item(self):
        self.fake("inventory_items/123456789", method="GET", body=self.load_fixture("inventory_item"))
        inventory_item = shopify.InventoryItem.find(123456789)
        self.assertEqual(inventory_item.sku, "IPOD2008PINK")

    def test_fetch_inventory_item_ids(self):
        self.fake(
            "inventory_items.json?ids=123456789%2C234567891",
            extension="",
            method="GET",
            body=self.load_fixture("inventory_items"),
        )
        inventory_items = shopify.InventoryItem.find(ids="123456789,234567891")
        self.assertEqual(3, len(inventory_items))
