from ..base import ShopifyResource


class Fulfillment(ShopifyResource):
    _prefix_source = "/admin/orders/$order_id/"

    def save(self):
        if 'order_id' not in self._prefix_options:
            self._prefix_options['order_id'] = self.order_id
        
        return super(ShopifyResource, self).save()

    def cancel(self):
        self._load_attributes_from_response(self.post("cancel"))

    def complete(self):
        self._load_attributes_from_response(self.post("complete"))

    def open(self):
        self._load_attributes_from_response(self.post("open"))
