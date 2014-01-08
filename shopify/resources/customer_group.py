from ..base import ShopifyResource
from customer import Customer

class CustomerGroup(ShopifyResource):
    def customers(cls, **kwargs):
        return Customer._build_list(cls.get("customers", **kwargs))