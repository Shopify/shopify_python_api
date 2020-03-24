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

        # github issue 347
        # todo: how to get the api version without split & strip
        api_version = ShopifyResource._site.split('/')[-1].strip('-')
        start_api_version = '201910'
        if api_version >= start_api_version:
            if self.attributes.get('inventory_quantity'):
                del self.attributes['inventory_quantity']
            if self.attributes.get('old_inventory_quantity'):
                del self.attributes['old_inventory_quantity']

        return super(ShopifyResource, self).save()
