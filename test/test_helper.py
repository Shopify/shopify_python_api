import os
import sys
import unittest
from pyactiveresource.activeresource import ActiveResource
from pyactiveresource.testing import http_fake
import shopify

class TestCase(unittest.TestCase):

    def setUp(self):
        ActiveResource.site = None
        ActiveResource.headers=None

        shopify.ShopifyResource.clear_session()
        shopify.ShopifyResource.site = "https://this-is-my-test-show.myshopify.com/admin/api/unstable"
        shopify.ShopifyResource.password = None
        shopify.ShopifyResource.user = None

        http_fake.initialize()
        self.http = http_fake.TestHandler
        self.http.set_response(Exception('Bad request'))
        self.http.site = 'https://this-is-my-test-show.myshopify.com'

    def load_fixture(self, name, format='json'):
        with open(os.path.dirname(__file__)+'/fixtures/%s.%s' % (name, format), 'rb') as f:
            return f.read()

    def fake(self, endpoint, **kwargs):
        body = kwargs.pop('body', None) or self.load_fixture(endpoint)
        format = kwargs.pop('format','json')
        method = kwargs.pop('method','GET')
        prefix = kwargs.pop('prefix', '/admin/api/unstable')

        if ('extension' in kwargs and not kwargs['extension']):
            extension = ""
        else:
            extension = ".%s" % (kwargs.pop('extension', 'json'))

        url = "https://this-is-my-test-show.myshopify.com%s/%s%s" % (prefix, endpoint, extension)
        try:
           url = kwargs['url']
        except KeyError:
           pass

        headers = {}
        if kwargs.pop('has_user_agent', True):
            userAgent = 'ShopifyPythonAPI/%s Python/%s' % (shopify.VERSION, sys.version.split(' ', 1)[0])
            headers['User-agent'] = userAgent

        try:
            headers.update(kwargs['headers'])
        except KeyError:
           pass

        code = kwargs.pop('code', 200)

        self.http.respond_to(
          method, url, headers, body=body, code=code)
