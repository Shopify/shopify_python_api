from ..base import ShopifyResource

class CustomerSavedSearch(ShopifyResource):
    def customers(cls, **kwargs):
        return Customer._build_list(cls.get("customers", **kwargs))