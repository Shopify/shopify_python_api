from ..base import ShopifyResource
from .usage_charge import UsageCharge


def _get_first_by_status(resources, status):
    for resource in resources:
        if resource.status == status:
            return resource
    return None


class RecurringApplicationCharge(ShopifyResource):
    def usage_charges(self):
        return UsageCharge.find(recurring_application_charge_id=self.id)

    def customize(self, **kwargs):
        self._load_attributes_from_response(self.put("customize", recurring_application_charge=kwargs))

    @classmethod
    def current(cls):
        """
        Returns first RecurringApplicationCharge object with status=active.
        If not found, None will be returned.
        """
        return _get_first_by_status(cls.find(), "active")

    def activate(self):
        self._load_attributes_from_response(self.post("activate"))
