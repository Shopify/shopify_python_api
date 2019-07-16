import shopify.resources
import shopify
import pdb
from shopify.pagination_link_headers import PaginationLinkHeaders

class Countable(object):

    @classmethod
    def count(cls, _options=None, **kwargs):
        if _options is None:
            _options = kwargs
        return int(cls.get("count", **_options))


class Metafields(object):

    def metafields(self, _options=None, **kwargs):
        if _options is None:
            _options = kwargs
        return shopify.resources.Metafield.find(resource=self.__class__.plural, resource_id=self.id, **_options)

    def metafields_count(self, _options=None, **kwargs):
        if _options is None:
            _options = kwargs
        return int(self.get("metafields/count", **_options))

    def add_metafield(self, metafield):
        if self.is_new():
            raise ValueError("You can only add metafields to a resource that has been saved")

        metafield._prefix_options = dict(resource=self.__class__.plural, resource_id=self.id)
        metafield.save()
        return metafield


class Events(object):

    def events(self):
        return shopify.resources.Event.find(resource=self.__class__.plural, resource_id=self.id)

class Pagination(object):

    def pagination_link_headers(self):
      self.pagination_link_headers = PaginationLinkHeaders()
      self._next_page_info = self.pagination_link_headers.link_headers

