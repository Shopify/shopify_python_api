from ..base import ShopifyResource
import shopify
import json


class InventoryLevel(ShopifyResource):

    def __repr__(self):
        return '%s(%s)' % (self._singular, self.available)

    @classmethod
    def adjust(cls, location_id, inventory_item_id, available_adjustment):
        body = {
            'inventory_item_id': inventory_item_id,
            'location_id': location_id,
            'available_adjustment': available_adjustment
        }
        resource = cls.post('adjust', body=json.dumps(body))
        return InventoryLevel(InventoryLevel.format.decode(resource.body))

    @classmethod
    def connect(cls, location_id, inventory_item_id, relocate_if_necessary=False, **kwargs):
        body = {
            'inventory_item_id': inventory_item_id,
            'location_id': location_id,
            'relocate_if_necessary': relocate_if_necessary,
        }
        resource = cls.post('connect', body=json.dumps(body))
        return InventoryLevel(InventoryLevel.format.decode(resource.body))

    @classmethod
    def set(cls, location_id, inventory_item_id, available, disconnect_if_necessary=False, **kwargs):
        body = {
            'inventory_item_id': inventory_item_id,
            'location_id': location_id,
            'available': available,
            'disconnect_if_necessary': disconnect_if_necessary,
        }
        resource = cls.post('set', body=json.dumps(body))
        return InventoryLevel(InventoryLevel.format.decode(resource.body))
