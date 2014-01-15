from ..base import ShopifyResource

class RecurringApplicationCharge(ShopifyResource):

    @classmethod
    def current(cls):
        return cls.find_first(status="active")

    def cancel(self):
        self._load_attributes_from_response(self.destroy)

    def activate(self):
        self._load_attributes_from_response(self.post("activate"))
