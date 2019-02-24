import shopify
from ..base import ShopifyResource


class ApiLimits(ShopifyResource):
    """
    API Calls Limit
    https://help.shopify.com/en/api/getting-started/api-call-limit

    HTTP_X_SHOPIFY_SHOP_API_CALL_LIMIT →1/40
    X-Shopify-Shop-Api-Call-Limit →1/40
    """
    API_LIMIT_HEADER_PARAM = "X-Shopify-Shop-Api-Call-Limit"
    # TODO: Add 429 Too Many Requests

    @classmethod
    def status(cls):
        status = str("0/0")
        # INFO: cls.connection.response is
        #       shopify.ShopifyResource.connection.response
        #       shopify.Shop.connection.response
        if not cls.connection.response:
            # raise ValueError("No shopify active sessions")
            shopify.Shop.current()

        # INFO: Suppress error
        #       AttributeError: 'NoneType' object has no attribute 'headers'
        _safe = getattr(cls.connection.response, "headers", '')

        if not _safe:
            raise ValueError("No shopify headers found")
        else:
            if cls.API_LIMIT_HEADER_PARAM in cls.connection.response.headers:
                status = str(cls.connection.response.headers[
                            cls.API_LIMIT_HEADER_PARAM])
        return status

    @classmethod
    def limit(cls):
        res = cls.status().split('/')
        return int(res[1])

    @classmethod
    def used(cls):
        res = cls.status().split('/')
        return int(res[0])

    @classmethod
    def left(cls):
        return int(cls.limit() - cls.used())
