from ..base import ShopifyResource

class UsageCharge(ShopifyResource):
    _prefix_source = "/recurring_application_charge/$recurring_application_charge_id/"

    @classmethod
    def _prefix(cls, options={}):
        recurring_application_charge_id = options.get("recurring_application_charge_id")
        if recurring_application_charge_id:
            return "%s/recurring_application_charges/%s" % (cls.site, recurring_application_charge_id)
        else:
            return cls.site
