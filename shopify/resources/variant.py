from ..base import ShopifyResource
from shopify import mixins


class Variant(ShopifyResource, mixins.Metafields):
    _prefix_source = "/products/$product_id/"

    @classmethod
    def _prefix(cls, options={}):
        product_id = options.get("product_id")
        if product_id:
            return "%s/products/%s" % (cls.site, product_id)
        else:
            return cls.site

    def save(self):
        if 'product_id' not in self._prefix_options:
            self._prefix_options['product_id'] = self.product_id
        return super(ShopifyResource, self).save()
