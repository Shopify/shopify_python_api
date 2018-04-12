from ..base import ShopifyResource


class GiftCardAdjustment(ShopifyResource):
    _prefix_source = "/admin/gift_cards/$gift_card_id/"
    _plural = 'adjustments'
    _singular = 'adjustment'
