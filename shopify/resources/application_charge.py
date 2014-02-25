from ..base import ShopifyResource


class ApplicationCharge(ShopifyResource):

    def activate(self):
        self._load_attributes_from_response(self.post("activate"))
