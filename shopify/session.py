import time
import urllib
import urllib2
try:
    from hashlib import md5
except ImportError:
    from md5 import md5
try:
    import simplejson as json
except ImportError:
    import json
import re


class Session(object):
    api_key = None
    secret = None
    protocol = 'https'

    @classmethod
    def setup(cls, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(cls, k, v)

    @classmethod
    def temp(cls, domain, token, block):
        session = Session(domain, token)
        import shopify
        original_domain = shopify.ShopifyResource.get_site()
        original_token = shopify.ShopifyResource.headers['X-Shopify-Access-Token']
        original_session = shopify.Session(original_domain, original_token)

        try:
            shopify.ShopifyResource.activate_session(session)
            return eval(block)
        finally:
            shopify.ShopifyResource.activate_session(original_session)

    def __init__(self, shop_url, token=None, params=None):
        self.url = self.__prepare_url(shop_url)
        self.token = token
        self.legacy = False
        return

    def create_permission_url(self, scope, redirect_uri=None):
        query_params = dict(client_id=self.api_key, scope=",".join(scope))
        if redirect_uri: query_params['redirect_uri'] = redirect_uri
        return "%s://%s/admin/oauth/authorize?%s" % (self.protocol, self.url, urllib.urlencode(query_params))

    def request_token(self, params):
        if self.token:
            return self.token

        if not self.validate_params(params):
            raise Exception('Invalid Signature: Possibly malicious login')

        code = params['code']

        url = "%s://%s/admin/oauth/access_token?" % (self.protocol, self.url)
        query_params = dict(client_id=self.api_key, client_secret=self.secret, code=code)
        request = urllib2.Request(url, urllib.urlencode(query_params))
        response = urllib2.urlopen(request)

        if response.code == 200:
            self.token = json.loads(response.read())['access_token']
            return self.token
        else:
            raise Exception(response.msg)

    @property
    def site(self):
        return "%s://%s/admin" % (self.protocol, self.url)

    @property
    def valid(self):
        return self.url is not None and self.token is not None

    @staticmethod
    def __prepare_url(url):
        if url.strip() == "":
            return None
        url = re.sub("https?://", "", url)
        url = re.sub("/.*", "", url)
        if url.find(".") == -1:
            url += ".myshopify.com"
        return url

    @classmethod
    def validate_params(cls, params):
        # Avoid replay attacks by making sure the request
        # isn't more than a day old.
        one_day = 24 * 60 * 60
        if int(params['timestamp']) < time.time() - one_day:
            return False

        return cls.validate_signature(params)

    @classmethod
    def validate_signature(cls, params):
        if "signature" not in params:
            return False

        sorted_params = ""
        signature = params['signature']

        for k in sorted(params.keys()):
            if k != "signature":
                sorted_params += k + "=" + str(params[k])

        return md5(cls.secret + sorted_params).hexdigest() == signature
