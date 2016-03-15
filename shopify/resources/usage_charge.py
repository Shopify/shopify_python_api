from ..base import ShopifyResource

class UsageCharge(ShopifyResource):
    _prefix_source = "/admin/recurring_application_charge/$recurring_application_charge_id/"

    @classmethod
    def _prefix(cls, options={}):
        recurring_application_charge_id = options.get("recurring_application_charge_id")
        if recurring_application_charge_id:
            return "/admin/recurring_application_charges/%s" % (recurring_application_charge_id)
        else:
            return "/admin"
