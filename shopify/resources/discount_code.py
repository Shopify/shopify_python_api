from ..base import ShopifyResource


'''
Discount Code for Price Rules API
'''
class DiscountCode(ShopifyResource):
    _prefix_source = "/admin/price_rules/$price_rule_id/"
