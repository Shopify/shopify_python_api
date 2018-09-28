from ..base import ShopifyResource
from .inventory_level import InventoryLevel

class Location(ShopifyResource):
    def inventory_levels(self, **kwargs):
        return InventoryLevel.find(from_="/admin/locations/%s/inventory_levels.json" % self.id, **kwargs)
