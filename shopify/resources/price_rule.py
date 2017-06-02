from ..base import ShopifyResource
from .discount_code import DiscountCode

class PriceRule(ShopifyResource):
    def add_discount_code(self, discount_code = DiscountCode()):
        resource = self.post("discount_codes", discount_code.encode())
        return DiscountCode(PriceRule.format.decode(resource.body))

    def discount_codes(self):
        return DiscountCode.find(price_rule_id=self.id)