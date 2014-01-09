from ..base import ShopifyResource
import shopify.mixins as mixins

class Customer(ShopifyResource, mixins.Metafields):
    @classmethod
    def search(cls, **kwargs):
        """Search for customers matching supplied query

        Args:
           q: Text to search for customers ("q" is short for query)
           f: Filters to apply to customers ("f" is short for query)
           page: Page to show (default: 1)
           limit: Maximum number of results to show (default: 50, maximum: 250)
        Returns:
           An array of customers.
        """
        return cls._build_list(cls.get("search", **kwargs))
