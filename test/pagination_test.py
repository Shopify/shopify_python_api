import shopify
import pdb
from mock import patch
from test.test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource
from pyactiveresource.util import xml_to_dict


class PaginationTest(TestCase):
    """
    API Calls Limit Tests

    Conversion of test/limits_test.rb
    """
    @classmethod
    def setUpClass(self):
        self.original_headers = None

    def setUp(self):
        super(PaginationTest, self).setUp()
        self.fake('shop')
        shopify.Shop.current()
        # TODO: Fake not support Headers
        self.original_headers = shopify.Shop.connection.response.headers

        self.next_page_info = "eyJkaXJlY3Rpb24iOiJuZXh0IiwibGFzdF9pZCI6NDQwMDg5NDIzLCJsYXN0X3ZhbHVlIjoiNDQwMDg5NDIzIn0%3D"
        self.previous_page_info = "eyJsYXN0X2lkIjoxMDg4MjgzMDksImxhc3RfdmFsdWUiOiIxMDg4MjgzMDkiLCJkaXJlY3Rpb24iOiJuZXh0In0%3D"

        # path_prefix = "%s/themes/%s" % (cls.site, theme_id) if theme_id else cls.site

        self.next_link_header = "<https://this-is-my-test-shop.myshopify.com/admin/api/unstable/draft_orders.json?page_info=%s>; rel=\"next\"" % self.next_page_info
        self.previous_link_header = "<https://this-is-my-test-shop.myshopify.com/admin/api/unstable/draft_orders.json?page_info=%s>; rel=\"previous\"" % self.previous_page_info


    def tearDown(self):
        super(PaginationTest, self).tearDown()
        shopify.Shop.connection.response.headers = self.original_headers

    def test_navigating_next_previous_orders(self):
        link_header = "%s, %s" % (self.previous_page_info, self.next_page_info)

        self.fake('draft_orders', method='GET', code=200, body=self.load_fixture('draft_orders'))
        draft_orders = shopify.DraftOrder.find()
        with patch.dict(
            shopify.Shop.connection.response.headers,
            {'Link': link_header},
            clear=True):

            xx = draft_orders[0].pagination_link_headers()
            pdb.set_trace()
            self.assertEqual(1, len(draft_orders))
            self.assertEqual(517119332, draft_orders[0].id)

