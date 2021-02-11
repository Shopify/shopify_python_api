from ..base import ShopifyResource


class Event(ShopifyResource):
    _prefix_source = "/$resource/$resource_id/"

    @classmethod
    def _prefix(cls, options={}):
        resource = options.get("resource")
        if resource:
            return "%s/%s/%s" % (cls.site, resource, options["resource_id"])
        else:
            return cls.site
