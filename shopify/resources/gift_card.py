from ..base import ShopifyResource
from .gift_card_adjustment import GiftCardAdjustment


class GiftCard(ShopifyResource):

    def disable(self):
        self._load_attributes_from_response(self.post("disable"))

    @classmethod
    def search(cls, **kwargs):
        """
        Search for gift cards matching supplied query

        Args:
           order: Field and direction to order results by (default: disabled_at DESC)
           query: Text to search for gift cards
           page: Page to show (default: 1)
           limit: Amount of results (default: 50) (maximum: 250)
           fields: comma-seperated list of fields to include in the response
        Returns:
           An array of gift cards.
        """
        return cls._build_list(cls.get("search", **kwargs))

    def add_adjustment(self, adjustment):
        """
        Create a new Gift Card Adjustment
        """
        resource = self.post("adjustments", adjustment.encode())
        return GiftCardAdjustment(GiftCard.format.decode(resource.body))
