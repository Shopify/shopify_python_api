from ..base import ShopifyResource
import shopify
import json


class InventoryLevel(ShopifyResource):
    def __repr__(self):
        return "%s(inventory_item_id=%s, location_id=%s)" % (self._singular, self.inventory_item_id, self.location_id)

    @classmethod
    def _element_path(cls, prefix_options={}, query_options=None):
        if query_options is None:
            prefix_options, query_options = cls._split_options(prefix_options)

        return "%s%s.%s%s" % (
            cls._prefix(prefix_options) + "/",
            cls.plural,
            cls.format.extension,
            cls._query_string(query_options),
        )

    @classmethod
    def adjust(cls, location_id, inventory_item_id, available_adjustment):
        body = {
            "inventory_item_id": inventory_item_id,
            "location_id": location_id,
            "available_adjustment": available_adjustment,
        }
        resource = cls.post("adjust", body=json.dumps(body).encode())
        return InventoryLevel(InventoryLevel.format.decode(resource.body))

    @classmethod
    def connect(cls, location_id, inventory_item_id, relocate_if_necessary=False, **kwargs):
        body = {
            "inventory_item_id": inventory_item_id,
            "location_id": location_id,
            "relocate_if_necessary": relocate_if_necessary,
        }
        resource = cls.post("connect", body=json.dumps(body).encode())
        return InventoryLevel(InventoryLevel.format.decode(resource.body))

    @classmethod
    def set(cls, location_id, inventory_item_id, available, disconnect_if_necessary=False, **kwargs):
        body = {
            "inventory_item_id": inventory_item_id,
            "location_id": location_id,
            "available": available,
            "disconnect_if_necessary": disconnect_if_necessary,
        }
        resource = cls.post("set", body=json.dumps(body).encode())
        return InventoryLevel(InventoryLevel.format.decode(resource.body))

    def is_new(self):
        return False

    def destroy(self):
        options = {"inventory_item_id": self.inventory_item_id, "location_id": self.location_id}
        return self.__class__.connection.delete(self._element_path(query_options=options), self.__class__.headers)
