import pdb
import shopify
class PaginationLinkHeaders(object):

    @classmethod
    def response(cls):
        if not shopify.Shop.connection.response:
             shopify.Shop.current()
        return shopify.Shop.connection.response


    def __init__(self):
        self._link_headers = self.parse_link_header(self.response().headers['Link'])
        self.next_link_header =

    def parse_link_header(self, link_header):
        pdb.set_trace()
        return 'aaa'


