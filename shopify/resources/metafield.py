from ..base import ShopifyResource

class Metafield(ShopifyResource):
    _prefix_source = "/admin/$resource/$resource_id/"

    @classmethod
    def _prefix(cls, options={}):
        return "/admin/" if options.get("resource") is None else "/admin/%s/%s" % (options["resource"], options["resource_id"])