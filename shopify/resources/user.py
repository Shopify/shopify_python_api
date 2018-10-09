from ..base import ShopifyResource


class User(ShopifyResource):

    @classmethod
    def current(cls):
        return User(cls.get('current'))
