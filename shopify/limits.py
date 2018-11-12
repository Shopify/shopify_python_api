import shopify

class Limits(object):
    CREDIT_LIMIT_HEADER_PARAM = 'x-shopify-shop-api-call-limit'

    @classmethod
    def credit_left(cls):
        return cls.credit_limit() - cls.credit_used()

    @classmethod
    def is_credit_maxed(cls):
        return cls.credit_left() <= 0

    @classmethod
    def credit_limit(cls):
        return int(cls._api_credit_limit_param()[1])

    @classmethod
    def credit_used(cls):
        return int(cls._api_credit_limit_param()[0])

    @classmethod
    def _api_credit_limit_param(cls):
        return cls._response().get(cls.CREDIT_LIMIT_HEADER_PARAM).split('/')

    @classmethod
    def _response(cls):
        if not shopify.ShopifyResource.connection.response:
            shopify.Shop.current()

        return shopify.ShopifyResource.connection.response
