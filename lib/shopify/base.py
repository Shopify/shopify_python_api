import pyactiveresource.util
import pyactiveresource.connection
from pyactiveresource.activeresource import ActiveResource, ResourceMeta
import shopify.yamlobjects
import shopify.mixins as mixins

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
        """HTTP connection which stores it's the last response"""
        super_class = cls.__mro__[1]
        if super_class == object or '_connection' in cls.__dict__:
            if cls._connection is None:
                cls._connection = ShopifyConnection(
                    cls.site, cls.user, cls.password, cls.timeout, cls.format)
            return cls._connection
        else:
            return super_class.connection

class ShopifyResource(ActiveResource, mixins.Countable):
    __metaclass__ = ShopifyResourceMeta
    _primary_key = "id"
    _connection = None

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
