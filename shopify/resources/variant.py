from ..base import ShopifyResource
from shopify import mixins

class Variant(ShopifyResource, mixins.Metafields):
    _prefix_source = "/admin/products/$product_id/"

    @classmethod
    def _prefix(cls, options={}):
        product_id = options.get("product_id")
        if product_id:
            return "/admin/products/%s" % (product_id)
        else:
            return "/admin/"
