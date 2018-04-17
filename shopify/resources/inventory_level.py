import json
from ..base import ShopifyResource


class InventoryLevel(ShopifyResource):
    @classmethod
    def _element_path(cls, id, prefix_options={}, query_options=None):
        if query_options is None:
            prefix_options, query_options = cls._split_options(prefix_options)

        return "%s%s.%s%s" % (cls._prefix(prefix_options)+'/', cls.plural,
                              cls.format.extension, cls._query_string(query_options))

    # TODO: ¯\_(ツ)_/¯
    # def destroy():
    #     self._load_attributes_from_response(
    #         self.destroy('/', location_id, inventory_item_id)
    #     )

    def connect(relocate_if_necessary=None):
        body_json = {'location_id': location_id, 'inventory_item_id': inventory_item_id}
        if relocate_if_necessary != None:
            body_json["relocate_if_necessary"] = relocate_if_necessary
        self._load_attributes_from_response(self.post('connect', {}, body_json.encode()))

    def set(new_available, disconnect_if_necessary=None):
        body_json = {
            'location_id': location_id,
            'inventory_item_id': inventory_item_id,
            'available': new_available
        }
        if disconnect_if_necessary != None:
            body_json["disconnect_if_necessary"] = disconnect_if_necessary
        self._load_attributes_from_response(self.post('set', {}, body_json.encode()))

    def adjust(available_adjustment):
        body_json = {
            'location_id': location_id,
            'inventory_item_id': inventory_item_id,
            'available_adjustment': available_adjustment
        }
        self._load_attributes_from_response(self.post('adjust', {},body_json.encode()))
