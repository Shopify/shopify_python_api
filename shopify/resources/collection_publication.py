from ..base import ShopifyResource


class CollectionPublication(ShopifyResource):
    _prefix_source = "/admin/publications/$publication_id/"
