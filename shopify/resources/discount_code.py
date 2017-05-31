from ..base import ShopifyResource

class DiscountCode(ShopifyResource):
    _prefix_source = "/admin/price_rules/$price_rule_id/"
