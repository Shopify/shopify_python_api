from ..base import ShopifyResource
from shopify import mixins


class Variant(ShopifyResource, mixins.Metafields):
    _prefix_source = "/admin/products/$product_id/"

    @classmethod
    def _prefix(cls, options={}):
        product_id = options.get("product_id")
        if options.get('is_new'):
            return "/admin/products/%s" % (product_id)
        else:
            return "/admin"

    @classmethod
    def find_first(cls, from_=None, sku=None, **kwargs):
        variant = None
        if sku:
            variants = cls._find_every(from_=from_, **kwargs)
            for v in variants:
                if v.sku == sku:
                    variant = v
                    break
        else:
            variant = ShopifyResource.find_first(cls, from_, **kwargs) 

        return variant

    def save(self):
        if 'product_id' not in self._prefix_options:
            self._prefix_options['product_id'] = self.product_id
        self._prefix_options['is_new'] = self.is_new()
        
        return super(ShopifyResource, self).save()

    def add_image(self, image):
        if not image.id:
            image.save()
        self.attributes['image_id'] = image.id
