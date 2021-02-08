from ..base import ShopifyResource

class ApplicationCredit(ShopifyResource):
    _prefix_source = "application_credits/$application_credit_id/"

    @classmethod
    def _prefix(cls, options={}):
        application_credit_id = options.get("application_credit_id")
        if application_credit_id:
            return "%s/application_credits/%s" % (cls.site, application_credit_id)
        else:
            return "%s" % (cls.site)
