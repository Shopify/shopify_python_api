from ..base import ShopifyResource

class ProductListing(ShopifyResource):
    _primary_key = "product_id"

    @classmethod
    def product_ids(cls, **kwargs):
        return cls.get('product_ids', **kwargs)
