from ..base import ShopifyResource


class ProductPublication(ShopifyResource):
    _prefix_source = "/admin/publications/$publication_id/"
