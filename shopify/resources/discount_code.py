from ..base import ShopifyResource


class DiscountCode(ShopifyResource):
    _prefix_source = "/price_rules/$price_rule_id/"
