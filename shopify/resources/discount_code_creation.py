from ..base import ShopifyResource
from .discount_code import DiscountCode

class DiscountCodeCreation(ShopifyResource):
    _prefix_source = "/admin/price_rules/$price_rule_id/"

    def discount_codes(self):
        return DiscountCode.find(from_="/admin/price_rules/%s/batch/%s/discount_codes.%s" % (self._prefix_options['price_rule_id'],
                                                                                             self.id,
                                                                                             DiscountCodeCreation.format.extension))
