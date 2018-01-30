from ..base import ShopifyResource


class ResourceFeedback(ShopifyResource):
    _prefix_source = "/admin/products/$product_id/"
    _plural = "resource_feedback"

    @classmethod
    def _prefix(cls, options={}):
        product_id = options.get("product_id")
        if product_id:
            return "/admin/products/%s" % product_id
        else:
            return "/admin"
