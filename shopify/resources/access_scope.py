from ..base import ShopifyResource


class AccessScope(ShopifyResource):
    @classmethod
    def override_prefix(cls):
        return "/admin/oauth"
