from ..base import ShopifyResource
import shopify.mixins as mixins

class Variant(ShopifyResource, mixins.Metafields):
    _prefix_source = "/admin/products/$product_id/"

    @classmethod
    def _prefix(cls, options={}):
        product_id = options.get("product_id")
        return "/admin/" if product_id is None else "/admin/products/%s" % (product_id)
