from ..base import ShopifyResource

class CustomerGroup(ShopifyResource):
    def customers(cls, **kwargs):
        return Customer._build_list(cls.get("customers", **kwargs))