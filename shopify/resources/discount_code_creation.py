from ..base import ShopifyResource
from .discount_code import DiscountCode


class DiscountCodeCreation(ShopifyResource):
    _prefix_source = "/price_rules/$price_rule_id/"

    def discount_codes(self):
        return DiscountCode.find(
            from_="%s/price_rules/%s/batch/%s/discount_codes.%s"
            % (
                ShopifyResource.site,
                self._prefix_options["price_rule_id"],
                self.id,
                DiscountCodeCreation.format.extension,
            )
        )
