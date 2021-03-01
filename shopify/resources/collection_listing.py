from ..base import ShopifyResource


class CollectionListing(ShopifyResource):
    _primary_key = "collection_id"

    def product_ids(cls, **kwargs):
        return cls.get("product_ids", **kwargs)
