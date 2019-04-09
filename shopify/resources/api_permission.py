from ..base import ShopifyResource

class ApiPermission(ShopifyResource):

    @classmethod
    def delete(cls):
        cls.connection.delete(cls.site + '/api_permissions/current.' + cls.format.extension, cls.headers)

    destroy = delete
