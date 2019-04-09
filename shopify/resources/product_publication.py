from ..base import ShopifyResource


class ProductPublication(ShopifyResource):
    _prefix_source = "/publications/$publication_id/"
