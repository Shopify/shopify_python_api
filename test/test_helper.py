import os
import sys
import unittest
from mock import patch
from pyactiveresource.activeresource import ActiveResource
from pyactiveresource.util import xml_to_dict
from pyactiveresource.testing import http_fake
import shopify

class TestCase(unittest.TestCase):

    def setUp(self):
        shopify.ShopifyResource.clear_session
        shopify.ShopifyResource.site = "http://localhost/admin"
        shopify.ShopifyResource.password = None
        shopify.ShopifyResource.user = None

        http_fake.initialize()
        self.http = http_fake.TestHandler
        self.http.set_response(Exception('Bad request'))
        self.http.site = 'https://localhost'

    def load_fixture(self, name, format='json'):
        return open(os.path.dirname(__file__)+'/fixtures/%s.%s' % (name, format), 'r').read()

    def fake(self, endpoint, **kwargs):
        body = kwargs.pop('body', None) or self.load_fixture(endpoint)
        format = kwargs.pop('format','json')
        method = kwargs.pop('method','GET')
        if ( 'extension' in kwargs and kwargs['extension'] == False ):
            extension = ""
        else:
            extension = ".%s" % (kwargs.pop('extension', None) or 'json')

        if 'url' in kwargs:
            url = kwargs['url']
        else:
            url = "http://localhost/admin/%s%s" %(endpoint,extension)

        headers = {}
        if kwargs.pop('userAgent', True): 
            userAgent = 'ShopifyPythonAPI/%s Python/%s' % (shopify.VERSION, sys.version.split(' ', 1)[0])
            headers['User-agent'] = userAgent

        if 'headers' in kwargs:
            if isinstance(kwargs['headers'], dict):
                headers.update(kwargs['headers'])

        code = kwargs.pop('code', 200)

        self.http.respond_to(
          method, url, headers, body = body, code = code)
