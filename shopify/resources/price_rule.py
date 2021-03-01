import json
from ..base import ShopifyResource
from .discount_code import DiscountCode
from .discount_code_creation import DiscountCodeCreation


class PriceRule(ShopifyResource):
    def add_discount_code(self, discount_code=DiscountCode()):
        resource = self.post("discount_codes", discount_code.encode())
        return DiscountCode(PriceRule.format.decode(resource.body))

    def discount_codes(self):
        return DiscountCode.find(price_rule_id=self.id)

    def create_batch(self, codes=[]):
        codes_json = json.dumps({"discount_codes": codes})

        response = self.post("batch", codes_json.encode())
        return DiscountCodeCreation(PriceRule.format.decode(response.body))

    def find_batch(self, batch_id):
        return DiscountCodeCreation.find_one(
            "%s/price_rules/%s/batch/%s.%s" % (ShopifyResource.site, self.id, batch_id, PriceRule.format.extension)
        )
