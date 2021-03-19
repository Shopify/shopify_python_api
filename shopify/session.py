import time
import hmac
import json
from hashlib import sha256

try:
    import simplejson as json
except ImportError:
    import json
import re
from contextlib import contextmanager
from six.moves import urllib
from shopify.api_access import ApiAccess
from shopify.api_version import ApiVersion, Release, Unstable
import six


class ValidationException(Exception):
    pass


class Session(object):
    api_key = None
    secret = None
    protocol = "https"
    myshopify_domain = "myshopify.com"
    port = None

    @classmethod
    def setup(cls, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(cls, k, v)

    @classmethod
    @contextmanager
    def temp(cls, domain, version, token):
        import shopify

        original_domain = shopify.ShopifyResource.url
        original_token = shopify.ShopifyResource.get_headers().get("X-Shopify-Access-Token")
        original_version = shopify.ShopifyResource.get_version() or version
        original_session = shopify.Session(original_domain, original_version, original_token)

        session = Session(domain, version, token)
        shopify.ShopifyResource.activate_session(session)
        yield
        shopify.ShopifyResource.activate_session(original_session)

    def __init__(self, shop_url, version=None, token=None, access_scopes=None):
        self.url = self.__prepare_url(shop_url)
        self.token = token
        self.version = ApiVersion.coerce_to_version(version)
        self.access_scopes = access_scopes
        return

    def create_permission_url(self, scope, redirect_uri, state=None):
        query_params = dict(client_id=self.api_key, scope=",".join(scope), redirect_uri=redirect_uri)
        if state:
            query_params["state"] = state
        return "https://%s/admin/oauth/authorize?%s" % (self.url, urllib.parse.urlencode(query_params))

    def request_token(self, params):
        if self.token:
            return self.token

        if not self.validate_params(params):
            raise ValidationException("Invalid HMAC: Possibly malicious login")

        code = params["code"]

        url = "https://%s/admin/oauth/access_token?" % self.url
        query_params = dict(client_id=self.api_key, client_secret=self.secret, code=code)
        request = urllib.request.Request(url, urllib.parse.urlencode(query_params).encode("utf-8"))
        response = urllib.request.urlopen(request)

        if response.code == 200:
            json_payload = json.loads(response.read().decode("utf-8"))
            self.token = json_payload["access_token"]
            self.access_scopes = json_payload["scope"]

            return self.token
        else:
            raise Exception(response.msg)

    @property
    def api_version(self):
        return self.version

    @property
    def site(self):
        return self.version.api_path("%s://%s" % (self.protocol, self.url))

    @property
    def valid(self):
        return self.url is not None and self.token is not None

    @property
    def access_scopes(self):
        return self._access_scopes

    @access_scopes.setter
    def access_scopes(self, scopes):
        if scopes is None or type(scopes) == ApiAccess:
            self._access_scopes = scopes
        else:
            self._access_scopes = ApiAccess(scopes)

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
        if int(params.get("timestamp", 0)) < time.time() - one_day:
            return False

        return cls.validate_hmac(params)

    @classmethod
    def validate_hmac(cls, params):
        if "hmac" not in params:
            return False

        hmac_calculated = cls.calculate_hmac(params).encode("utf-8")
        hmac_to_verify = params["hmac"].encode("utf-8")

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
                if k == "hmac":
                    continue

                if k.endswith("[]"):
                    # foo[]=1&foo[]=2 has to be transformed as foo=["1", "2"] note the whitespace after comma
                    k = k.rstrip("[]")
                    v = json.dumps(list(map(str, v)))

                # escape delimiters to avoid tampering
                k = str(k).replace("%", "%25").replace("=", "%3D")
                v = str(v).replace("%", "%25")
                yield "{0}={1}".format(k, v).replace("&", "%26")

        return "&".join(sorted(encoded_pairs(params)))
