from ..base import ShopifyResource
from shopify import mixins
from .customer_invite import CustomerInvite


class Customer(ShopifyResource, mixins.Metafields):

    @classmethod
    def search(cls, **kwargs):
        """
        Search for customers matching supplied query

        Args:
           order: Field and direction to order results by (default: last_order_date DESC)
           query: Text to search for customers
           page: Page to show (default: 1)
           limit: Amount of results (default: 50) (maximum: 250)
           fields: comma-seperated list of fields to include in the response
        Returns:
           An array of customers.
        """
        return cls._build_list(cls.get("search", **kwargs))

    def send_invite(self, customer_invite = CustomerInvite()):
        resource = self.post("send_invite", customer_invite.encode())
        return CustomerInvite(Customer.format.decode(resource.body))
