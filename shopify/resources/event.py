from ..base import ShopifyResource

class Event(ShopifyResource):
    _prefix_source = "/admin/$resource/$resource_id/"

    @classmethod
    def _prefix(cls, options={}):
        resource = options.get("resource")
        if resource:
            return "/admin/%s/%s" % (resource, options["resource_id"])
        else:
            return "/admin"
