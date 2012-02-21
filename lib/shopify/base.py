import pyactiveresource.util
import pyactiveresource.connection
from pyactiveresource.activeresource import ActiveResource, ResourceMeta
import shopify.yamlobjects
import shopify.mixins as mixins
import threading
import urllib
import urllib2
import urlparse

# Store the response from the last request in the connection object
class ShopifyConnection(pyactiveresource.connection.Connection):
    response = None
    def _open(self, *args, **kwargs):
        self.response = None
        try:
            self.response = super(ShopifyConnection, self)._open(*args, **kwargs)
        except pyactiveresource.connection.ConnectionError, err:
            self.response = err.response
            raise
        return self.response

# Inherit from pyactiveresource's metaclass in order to use ShopifyConnection
class ShopifyResourceMeta(ResourceMeta):
    @property
    def connection(cls):
        """HTTP connection for the current thread"""
        super_class = cls.__mro__[1]
        local = cls._threadlocal
        if not getattr(local, 'connection', None):
            # Make sure these variables are no longer affected by other threads.
            local.user = cls.user
            local.password = cls.password
            local.site = cls.site
            local.timeout = cls.timeout
            local.connection = ShopifyConnection(
                cls.site, cls.user, cls.password, cls.timeout, cls.format)
        return local.connection

    def get_user(cls):
        return getattr(cls._threadlocal, 'user', ShopifyResource._user)

    def set_user(cls, value):
        cls._threadlocal.connection = None
        ShopifyResource._user = cls._threadlocal.user = value

    user = property(get_user, set_user, None,
                    "The username for HTTP Basic Auth.")

    def get_password(cls):
        return getattr(cls._threadlocal, 'password', ShopifyResource._password)

    def set_password(cls, value):
        cls._threadlocal.connection = None
        ShopifyResource._password = cls._threadlocal.password = value

    password = property(get_password, set_password, None,
                        "The password for HTTP Basic Auth.")

    def get_site(cls):
        return getattr(cls._threadlocal, 'site', ShopifyResource._site)

    def set_site(cls, value):
        cls._threadlocal.connection = None
        ShopifyResource._site = cls._threadlocal.site = value
        if value is not None:
            host = urlparse.urlsplit(value)[1]
            auth_info, host = urllib2.splituser(host)
            if auth_info:
                user, password = urllib2.splitpasswd(auth_info)
                if user:
                    cls.user = urllib.unquote(user)
                if password:
                    cls.password = urllib.unquote(password)

    site = property(get_site, set_site, None,
                    'The base REST site to connect to.')

    def get_timeout(cls):
        return getattr(cls._threadlocal, 'timeout', ShopifyResource._timeout)

    def set_timeout(cls, value):
        cls._threadlocal.connection = None
        ShopifyResource._timeout = cls._threadlocal.timeout = value

    timeout = property(get_timeout, set_timeout, None,
                       'Socket timeout for HTTP requests')


class ShopifyResource(ActiveResource, mixins.Countable):
    __metaclass__ = ShopifyResourceMeta
    _primary_key = "id"
    _threadlocal = threading.local()

    def __init__(self, attributes=None, prefix_options=None):
        if attributes is not None and prefix_options is None:
            prefix_options, attributes = self.__class__._split_options(attributes)
        return super(ShopifyResource, self).__init__(attributes, prefix_options)

    def is_new(self):
        return not self.id

    def _load_attributes_from_response(self, response):
        self._update(self.__class__.format.decode(response.body))

    def encode(self, options):
        # pyactiveresource (version 1.0.1) doesn't support encoding to_json
        return pyactiveresource.util.to_xml(options)

    def __get_primary_key(self):
        return self._primary_key

    def __set_primary_key(self, value):
        self._primary_key = value

    primary_key = property(__get_primary_key, __set_primary_key, None,
                           'Primary key to identity the resource (defaults to "id")')

    def __get_id(self):
        if self._primary_key != "id":
            return getattr(self, self._primary_key)
        else:
            return super(ShopifyResource, self).__getattr__("id")

    def __set_id(self, value):
        if self._primary_key != "id":
            return setattr(self, self._primary_key, value)
        else:
            return super(ShopifyResource, self).__setattr__("id", value)

    id = property(__get_id, __set_id, None, 'Value stored in the primary key')

    def save(self):
        # See pyactiveresource issue 14: http://code.google.com/p/pyactiveresource/issues/detail?id=14
        self.errors.clear()
        return super(ShopifyResource, self).save()
