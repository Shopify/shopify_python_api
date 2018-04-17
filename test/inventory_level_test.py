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

        # TODO: this doesn't work because urlencode generates the query string as location_ids=['123', '456']
        # while pyactiveresource generates the query string as location_ids[]=123&location_ids[]=456
        # self.fake("inventory_levels.json?" + urllib.urlencode(params, True), extension=False, method='GET', status=200, body=self.load_fixture('inventory_levels'))

        # this works but it's ugly
        self.fake(
            "inventory_levels.json?location_ids%5B%5D=905684977&location_ids%5B%5D=487838322&inventory_item_ids%5B%5D=808950810&inventory_item_ids%5B%5D=39072856",
            extension=False,
            method='GET',
            status=200,
            body=self.load_fixture('inventory_levels')
        )
        inventory_levels = shopify.InventoryLevel.find(inventory_item_ids=[808950810, 39072856], location_ids=[905684977, 487838322])

        self.assertTrue(
            all(item.location_id in params['location_ids'] and item.inventory_item_id in params['inventory_item_ids'] for item in inventory_levels)
        )

    # TODO: below tests appear to be erroneously hitting
    # https://this-is-my-test-show.myshopify.com/admin/inventory_levels/new/{action}.json
    # rather than https://this-is-my-test-show.myshopify.com/admin/inventory_levels/{action}.json

    def test_adjust_with_adjustment_value(self):
        adjustment = 5
        updated_available = self.inventory_level.available + adjustment
        self.inventory_level_response['available'] = updated_available

        self.fake('inventory_levels/adjust', method='POST', body=json.dumps(self.inventory_level_response))
        self.inventory_level.adjust(adjustment)
        self.assertEqual(updated_available, self.inventory_level.available)

    def test_connect_saves_inventory_level(self):
        params = {'inventory_item_id': 808950810, 'location_id': 99999999}
        response = params.copy()
        response['available'] = 0

        self.fake('inventory_lvels/connect', method='POST', body=json.dumps(response))
        inventory_level = shopify.InventoryLevel(params)
        inventory_level.connect()
        self.assertEqual(0, inventory_level.available)

    def test_destroy_removes_inventory_level(self):
        params = {
            'inventory_item_id': self.inventory_level.inventory_item_id,
            'location_id': self.inventory_level.location_id
        }

        query_params = urllib.urlencode(params)
        path = "inventory_levels.json" + query_params

        # TODO: pyactiveresource doesn't like body=None or body={} ...? I don't think the body matters anyway
        self.fake(path, extension=False, method='DELETE', status=204, body=json.dumps(self.inventory_level_response))

        # TODO: TypeError: destroy() takes exactly 1 argument (4 given)
        self.assertEqual(self.inventory_level.destroy(), None)

    def test_set_with_available_value(self):
        available = 13
        response = self.inventory_level_response.copy()
        response['inventory_level']['available'] = available

        self.fake('inventory_levels/set', method='POST', body=json.dumps(response))
        self.inventory_level.set(available, response.)

        self.assertEqual(available, self.inventory_level.available)