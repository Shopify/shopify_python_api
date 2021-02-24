from ..base import ShopifyResource
from .customer import Customer


class CustomerSavedSearch(ShopifyResource):
    def customers(cls, **kwargs):
        return Customer._build_collection(cls.get("customers", **kwargs))
