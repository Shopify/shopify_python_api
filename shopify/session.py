import pyactiveresource.formats
import time
import urllib
try:
    from hashlib import md5
except ImportError:
    from md5 import md5
try:
    import simplejson as json
except ImportError:
    import json
import re

# Partial JSON support needed only for authentication.
# Full JSON support requires a patch sent upstream to pyactiveresource.
class JSONFormat(pyactiveresource.formats.Base):
    extension = 'json'
    mime_type = 'application/json'

    @staticmethod
    def decode(resource_string):
        data = json.loads(resource_string)
        if isinstance(data, dict) and len(data) == 1:
            return data.values()[0]
        return data

class ValidationException(Exception):
    pass

class Session(object):
    api_key = None
    secret = None
    protocol = 'https'

    @classmethod
    def setup(cls, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(cls, k, v)

    def __init__(self, shop_url, params=None):
        self.url = self.__prepare_url(shop_url)
        self.token = None
        self.legacy = False

        if params is None:
            return

        if not self.validate_params(params):
            raise ValidationException('Invalid Signature: Possibly malicious login')

        if params.has_key('code'):
            # OAuth2
            self.token = self.request_token(params['code'])
        else:
            # Legacy
            self.legacy = True
            self.token = self.__computed_password(params['t'])

    def shop(self):
        Shop.current()

    @classmethod
    def create_permission_url(cls, shop_url, scope=None, redirect_uri=None):
        shop_url = cls.__prepare_url(shop_url)
        if scope:
            # OAuth2
            query_params = dict(client_id=cls.api_key, scope=",".join(scope))
            if redirect_uri: query_params['redirect_uri'] = redirect_uri
            return "%s://%s/admin/oauth/authorize?%s" % (cls.protocol, shop_url, urllib.urlencode(query_params))
        else:
            # Legacy
            return "%s://%s/admin/api/auth?api_key=%s" % (cls.protocol, shop_url, cls.api_key)

    @property
    def site(self):
        if self.legacy:
            # deprecated backwards compatiblity for setting ShopifyResource.site directly
            return "%s://%s:%s@%s/admin" % (self.protocol, self.api_key, self.token, self.url)
        else:
            return "%s://%s/admin" % (self.protocol, self.url)

    def request_token(self, code):
        from shopify.base import ShopifyResource, ShopifyConnection
        if self.token:
            return self.token
        site = "%s://%s" % (self.protocol, self.url)
        params = (self.api_key, self.secret, code)
        access_token_path = "/admin/oauth/access_token?client_id=%s&client_secret=%s&code=%s" % params
        connection = ShopifyConnection(site, None, None, ShopifyResource.timeout, JSONFormat)
        response = connection.post(access_token_path, ShopifyResource.headers)
        body = json.loads(response.body)
        if response.code == 200:
            self.token = body['access_token']
            return self.token
        else:
            raise response.response

    def __computed_password(self, t):
        return md5(self.secret + t).hexdigest()

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
                sorted_params += k + "=" + params[k]

        return md5(cls.secret + sorted_params).hexdigest() == signature
