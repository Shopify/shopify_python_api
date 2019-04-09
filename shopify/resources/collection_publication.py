from ..base import ShopifyResource


class CollectionPublication(ShopifyResource):
    _prefix_source = "/publications/$publication_id/"
