import os
import sys
import unittest
from pyactiveresource.tests import http_fake
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

        userAgent = 'ShopifyPythonAPI/%s Python/%s' % (shopify.VERSION, sys.version.split(' ', 1)[0])
        headers = {'User-agent': userAgent}

        if method == 'POST':
            headers['Content-type'] = 'application/%s' % format

        self.http.respond_to(
          method, url, headers, body = body, code = 200)

# require 'rubygems'
# require 'test/unit'
# require 'fakeweb'
# require 'mocha'

# $LOAD_PATH.unshift(File.dirname(__FILE__))
# $LOAD_PATH.unshift(File.join(File.dirname(__FILE__), '..', 'lib'))
# require 'shopify_api'

# FakeWeb.allow_net_connect = false

# # setup ShopifyAPI with fake api_key and secret

# class Test::Unit::TestCase
#   def self.test(string, &block)
#     define_method("test:#{string}", &block)
#   end

#   def self.should(string, &block)
#     self.test("should_#{string}", &block)
#   end
  
#   def self.context(string)
#     yield
#   end

#   def setup
#     ActiveResource::Base.format = :json
#     ShopifyAPI.constants.each do |const|
#       begin
#         const = "ShopifyAPI::#{const}".constantize
#         const.format = :json if const.respond_to?(:format=)
#       rescue NameError
#       end
#     end

#     ShopifyAPI::Base.clear_session
#     ShopifyAPI::Base.site = "http://localhost/admin"
#     ShopifyAPI::Base.password = nil
#     ShopifyAPI::Base.user = nil
#   end

#   def teardown
#     FakeWeb.clean_registry
#   end
  
#   # Custom Assertions
#   def assert_not(expression)
#     assert_block("Expected <#{expression}> to be false!") { not expression }
#   end