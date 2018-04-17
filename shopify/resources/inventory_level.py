from ..base import ShopifyResource
import json


class InventoryLevel(ShopifyResource):
    #@classmethod
    #def _prefix(cls, options={}):
    #    return "/admin"

    @classmethod
    def _element_path(cls, id, prefix_options={}, query_options=None):
        if query_options is None:
            prefix_options, query_options = cls._split_options(prefix_options)

        return "%s%s.%s%s" % (cls._prefix(prefix_options)+'/', cls.plural,
                              cls.format.extension, cls._query_string(query_options))

    # TODO: Need this?
    # def is_new(self):
    #     return False

    # TODO: hmmm
    #def destroy(self):
    #    self._load_attributes_from_response(
    #        self.destroy('/', location_id=self.location_id, inventory_item_id=self.inventory_item_id)
    #    )

    def connect(cls, location_id, inventory_item_id, relocate_if_necessary=None, **kwargs):
        body_json = json.dumps({'location_id': location_id, 'inventory_item_id': inventory_item_id})
        if relocate_if_necessary != None:
            body_json["relocate_if_necessary"] = relocate_if_necessary
        cls._load_attributes_from_response(cls.post('connect', body_json.encode()))

    def set(cls, location_id, inventory_item_id, new_available, disconnect_if_necessary=None):
        body_json = json.dumps({
            'location_id': location_id,
            'inventory_item_id': inventory_item_id,
            'available': new_available
        })
        if disconnect_if_necessary != None:
            body_json["disconnect_if_necessary"] = disconnect_if_necessary
        cls._load_attributes_from_response(cls.post('set', body_json.encode()))

    def adjust(cls, location_id, inventory_item_id, available_adjustment):
        body_json = json.dumps({
            'location_id': location_id,
            'inventory_item_id': inventory_item_id,
            'available_adjustment': available_adjustment
        })
        cls._load_attributes_from_response(cls.post('adjust', body_json.encode()))
