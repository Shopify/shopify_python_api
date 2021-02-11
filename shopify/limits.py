import shopify


class Limits(object):
    """
    API Calls Limit
    https://help.shopify.com/en/api/getting-started/api-call-limit

    Conversion of lib/shopify_api/limits.rb
    """

    # num_requests_executed/max_requests
    # Eg: 1/40
    CREDIT_LIMIT_HEADER_PARAM = "X-Shopify-Shop-Api-Call-Limit"

    @classmethod
    def response(cls):
        if not shopify.Shop.connection.response:
            shopify.Shop.current()
        return shopify.Shop.connection.response

    @classmethod
    def api_credit_limit_param(cls):
        response = cls.response()
        _safe_header = getattr(response, "headers", "")

        if not _safe_header:
            raise Exception("No shopify headers found")

        if cls.CREDIT_LIMIT_HEADER_PARAM in response.headers:
            credits = response.headers[cls.CREDIT_LIMIT_HEADER_PARAM]
            return credits.split("/")
        else:
            raise Exception("No valid api call header found")

    @classmethod
    def credit_left(cls):
        """
        How many more API calls can I make?
        """
        return int(cls.credit_limit() - cls.credit_used())

    @classmethod
    def credit_maxed(cls):
        """
        Have I reached my API call limit?
        """
        return bool(cls.credit_left() <= 0)

    @classmethod
    def credit_limit(cls):
        """
        How many total API calls can I make?
        """
        return int(cls.api_credit_limit_param()[1])

    @classmethod
    def credit_used(cls):
        """
        How many API calls have I made?
        """
        return int(cls.api_credit_limit_param()[0])
