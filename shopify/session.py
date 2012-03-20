import time
try:
    from hashlib import md5
except ImportError:
    from md5 import md5
import re

class ValidationException(Exception):
    pass

class Session(object):
    """The Session helps in authenticating an API session.

    The Shopify API authenticates each call via HTTP Authentication, using
      * the application's API key as the username, and
      * a hex digest of the application's shared secret and an
        authentication token as the password.

    Generation & acquisition of the beforementioned looks like this:

      0. Developer (that's you) registers Application (and provides a
         callback url) and receives an API key and a shared secret

      1. User visits Application and are told they need to authenticate the
         application first for read/write permission to their data (needs to
         happen only once). User is asked for their shop url.

      2. Application redirects to Shopify : GET <user's shop url>/admin/api/auth?api_key=<API key>
         (See Session.create_permission_url)

      3. User logs-in to Shopify, approves application permission request

      4. Shopify redirects to the Application's callback url (provided during
         registration), including the shop's name, and an authentication token in the parameters:
           GET client.com/customers?shop=snake-oil.myshopify.com&t=a94a110d86d2452eb3e2af4cfb8a3828

      5. Authentication password computed using the shared secret and the
         authentication token (see Session.__computed_password)

      6. Profit!
         (API calls can now authenticate through HTTP using the API key, and
         computed password)

    The Session.site method can be used to set ShopifyResource.site,
    so that all API calls are authorized transparently and end up
    just looking like this:

      # get 3 products
      products = shopify.Product.find(limit=3)

      # get latest 3 orders
      orders = shopify.Order.find(limit=3, order="created_at DESC")
    """
    api_key = None
    secret = None
    protocol = 'https'

    @classmethod
    def setup(cls, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(cls, k, v)

    def __init__(self, shop_url, params=None, **kwargs):
        if params is None:
            params = kwargs
        self.url = self.__prepare_url(shop_url)
        self.token = params.get('t')
        self.name = None

        if not self.__validate_signature(params) or \
           not int(params['timestamp']) > time.time() - 24 * 60 * 60:
            raise ValidationException('Invalid Signature: Possibly malicious login')

    def shop(self):
        Shop.current()

    @classmethod
    def create_permission_url(cls, shop_url):
        shop_url = cls.__prepare_url(shop_url)
        return "%s://%s/admin/api/auth?api_key=%s" % (cls.protocol, shop_url, cls.api_key)

    @property
    def site(self):
        return "%s://%s:%s@%s/admin" % (self.protocol, self.api_key, self.__computed_password(), self.url)

    def __computed_password(self):
        return md5(self.secret + self.token).hexdigest()

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
    def __validate_signature(cls, params):
        if "signature" not in params:
            return False

        sorted_params = ""
        signature = params['signature']

        for k in sorted(params.keys()):
            if k != "signature":
                sorted_params += k + "=" + params[k]

        return md5(cls.secret + sorted_params).hexdigest() == signature
