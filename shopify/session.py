import time
import hmac
from hashlib import sha256
try:
    import simplejson as json
except ImportError:
    import json
import re
from contextlib import contextmanager
from six.moves import urllib
import six

class ValidationException(Exception):
    pass

class Session(object):
    api_key = None
    secret = None
    protocol = 'https'
    myshopify_domain = 'myshopify.com'
    port = None

    @classmethod
    def setup(cls, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(cls, k, v)

    @classmethod
    @contextmanager
    def temp(cls, domain, token):
        import shopify
        original_site = shopify.ShopifyResource.get_site()
        original_token = shopify.ShopifyResource.get_headers().get('X-Shopify-Access-Token')
        original_session = shopify.Session(original_site, original_token)

        session = Session(domain, token)
        shopify.ShopifyResource.activate_session(session)
        yield
        shopify.ShopifyResource.activate_session(original_session)

    def __init__(self, shop_url, token=None, params=None):
        self.url = self.__prepare_url(shop_url)
        self.token = token
        return

    def create_permission_url(self, scope, redirect_uri=None):
        query_params = dict(client_id=self.api_key, scope=",".join(scope))
        if redirect_uri: query_params['redirect_uri'] = redirect_uri
        return "%s/oauth/authorize?%s" % (self.site, urllib.parse.urlencode(query_params))

    def request_token(self, params):
        if self.token:
            return self.token

        if not self.validate_params(params):
            raise ValidationException('Invalid HMAC: Possibly malicious login')

        code = params['code']

        url = "%s/oauth/access_token?" % self.site
        query_params = dict(client_id=self.api_key, client_secret=self.secret, code=code)
        request = urllib.request.Request(url, urllib.parse.urlencode(query_params).encode('utf-8'))
        response = urllib.request.urlopen(request)

        if response.code == 200:
            self.token = json.loads(response.read().decode('utf-8'))['access_token']
            return self.token
        else:
            raise Exception(response.msg)

    @property
    def site(self):
        return "%s://%s/admin" % (self.protocol, self.url)

    @property
    def valid(self):
        return self.url is not None and self.token is not None

    @classmethod
    def __prepare_url(cls, url):
        if not url or (url.strip() == ""):
            return None
        url = re.sub("^https?://", "", url)
        shop = urllib.parse.urlparse("https://" + url).hostname
        if shop is None:
            return None
        idx = shop.find(".")
        if idx != -1:
            shop = shop[0:idx]
        if len(shop) == 0:
            return None
        shop += "." + cls.myshopify_domain
        if cls.port:
            shop += ":" + str(cls.port)
        return shop

    @classmethod
    def validate_params(cls, params):
        # Avoid replay attacks by making sure the request
        # isn't more than a day old.
        one_day = 24 * 60 * 60
        if int(params.get('timestamp', 0)) < time.time() - one_day:
            return False

        return cls.validate_hmac(params)

    @classmethod
    def validate_hmac(cls, params):
        if 'hmac' not in params:
            return False

        hmac_calculated = cls.calculate_hmac(params).encode('utf-8')
        hmac_to_verify = params['hmac'].encode('utf-8')

        # Try to use compare_digest() to reduce vulnerability to timing attacks.
        # If it's not available, just fall back to regular string comparison.
        try:
            return hmac.compare_digest(hmac_calculated, hmac_to_verify)
        except AttributeError:
            return hmac_calculated == hmac_to_verify

    @classmethod
    def calculate_hmac(cls, params):
        """
        Calculate the HMAC of the given parameters in line with Shopify's rules for OAuth authentication.
        See http://docs.shopify.com/api/authentication/oauth#verification.
        """
        encoded_params = cls.__encoded_params_for_signature(params)
        # Generate the hex digest for the sorted parameters using the secret.
        return hmac.new(cls.secret.encode(), encoded_params.encode(), sha256).hexdigest()

    @classmethod
    def __encoded_params_for_signature(cls, params):
        """
        Sort and combine query parameters into a single string, excluding those that should be removed and joining with '&'
        """
        def encoded_pairs(params):
            for k, v in six.iteritems(params):
                if k != 'hmac':
                    # escape delimiters to avoid tampering
                    k = str(k).replace("%", "%25").replace("=", "%3D")
                    v = str(v).replace("%", "%25")
                    yield '{0}={1}'.format(k, v).replace("&", "%26")

        return "&".join(sorted(encoded_pairs(params)))
