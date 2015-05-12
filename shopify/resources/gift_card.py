from ..base import ShopifyResource


class GiftCard(ShopifyResource):

    def disable(self):
        self._load_attributes_from_response(self.post("disable"))
