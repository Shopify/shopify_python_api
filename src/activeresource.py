#!/usr/bin/python2.4
# Authors: Jared Kuolt <me@superjared.com>, Mark Roach <mrroach@google.com>

"""Connect to and interact with a REST server and its objects."""


import new
import re
import sys
import urllib
import urllib2
import urlparse
from string import Template
from pyactiveresource import connection
from pyactiveresource import formats
from pyactiveresource import util


VALID_NAME = re.compile('[a-z_]\w*')  # Valid python attribute names


class Error(Exception):
    """A general error derived from Exception."""
    pass


class Errors(object):
    """Represents error lists returned by the server."""

    def __init__(self, base):
        """Constructor for Errors object.

        Args:
            base: The parent resource object.
        """
        self.base = base
        self.errors = {}

    @property
    def size(self):
        return len(self.errors)

    def __len__(self):
        return len(self.errors)

    def add(self, attribute, error):
        """Add an error to a resource object's attribute.

        Args:
            attribute: The attribute to add the error to.
            error: The error string to add.
        Returns:
            None
        """
        self.errors.setdefault(attribute, []).append(error)

    def add_to_base(self, error):
        """Add an error to the base resource object rather than an attribute.

        Args:
            error: the error string to add.
        Returns:
            None
        """
        self.add('base', error)

    def clear(self):
        """Clear any errors that have been set.

        Args:
            None
        Returns:
            None
        """
        self.errors = {}

    def from_xml(self, xml_string):
        """Grab errors from an XML response.

        Args:
            xml_string: An xml errors object (e.g. '<errors></errors>')
        Returns:
            None
        """
        attribute_keys = self.base.attributes.keys()
        try:
            messages = util.xml_to_dict(
                    xml_string, saveroot=True)['errors']['error']
            if not isinstance(messages, list):
                messages = [messages]
        except util.Error:
            messages = []
        for message in messages:
            attr_name = message.split()[0]
            key = util.underscore(attr_name)
            if key in attribute_keys:
                self.add(key, message[len(attr_name)+1:])
            else:
                self.add_to_base(message)

    def on(self, attribute):
        """Return the errors for the given attribute.

        Args:
            attribute: The attribute to retrieve errors for.
        Returns:
            An error string, or a list of error message strings or None
            if none exist for the given attribute.
        """
        errors = self.errors.get(attribute, [])
        if len(errors) == 1:
            return errors[0]
        return errors

    def full_messages(self):
        """Returns all the full error messages in an array.

        Args:
            None
        Returns:
            An array of error strings.
        """
        messages = []
        for key, errors in self.errors.items():
            for error in errors:
                if key == 'base':
                    messages.append(error)
                else:
                    messages.append(' '.join((key, error)))
        return messages


class ClassAndInstanceMethod(object):
    """A descriptor to allow class/instance methods with the same name."""

    def __init__(self, class_method, instance_method):
        self.class_method = class_method
        self.instance_method = instance_method

    def __get__(self, instance, owner):
        if instance:
            return getattr(instance, self.instance_method)
        return getattr(owner, self.class_method)


class ResourceMeta(type):
    """A metaclass for ActiveResource objects.

    Provides a separate namespace for configuration objects (user,password,
    site, etc)"""

    def __new__(mcs, name, bases, new_attrs):
        """Create a new class.

        Args:
            mcs: The metaclass.
            name: The name of the class.
            bases: List of base classes from which mcs inherits.
            new_attrs: The class attribute dictionary.
        """
        if '_singular' not in new_attrs or not new_attrs['_singular']:
            # Convert CamelCase to lower_underscore
            singular = re.sub(r'\B((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))',
                              r'_\1', name).lower()
            new_attrs['_singular'] = singular

        if '_plural' not in new_attrs or not new_attrs['_plural']:
            new_attrs['_plural'] = util.pluralize(new_attrs['_singular'])


        klass = type.__new__(mcs, name, bases, new_attrs)

        # if _site is defined, use the site property to ensure that user
        # and password are properly initialized.
        if '_site' in new_attrs:
            klass.site = new_attrs['_site']

        return klass

    @property
    def connection(cls):
        """A connection object which handles all HTTP requests."""
        super_class = cls.__mro__[1]
        if super_class == object or '_connection' in cls.__dict__:
            if cls._connection is None:
                cls._connection = connection.Connection(
                    cls.site, cls.user, cls.password, cls.timeout, cls.format)
            return cls._connection
        else:
            return super_class.connection

    def get_user(cls):
        return cls._user

    def set_user(cls, value):
      cls._connection = None
      cls._user = value

    user = property(get_user, set_user, None,
                    'A username for HTTP Basic Auth.')

    def get_password(cls):
        return cls._password

    def set_password(cls, value):
        cls._connection = None
        cls._password = value

    password = property(get_password, set_password, None,
                        'A password for HTTP Basic Auth.')

    def get_site(cls):
        return cls._site

    def set_site(cls, value):
        if value is not None:
            host = urlparse.urlsplit(value)[1]
            auth_info, host = urllib2.splituser(host)
            if auth_info:
                user, password = urllib2.splitpasswd(auth_info)
                if user:
                    cls._user = urllib.unquote(user)
                if password:
                    cls._password = urllib.unquote(password)
        cls._connection = None
        cls._site = value

    site = property(get_site, set_site, None,
                    'The base REST site to connect to.')

    def get_headers(cls):
        return cls._headers

    def set_headers(cls, value):
        cls._headers = value
    headers = property(get_headers, set_headers, None,
                       'HTTP headers.')

    def get_timeout(cls):
        return cls._timeout

    def set_timeout(cls, value):
        cls._connection = None
        cls._timeout = value
    timeout = property(get_timeout, set_timeout, None,
                       'Socket timeout for HTTP operations')

    def get_format(cls):
        return cls._format

    def set_format(cls, value):
        cls._format = value
    format = property(get_format, set_format, None,
                       'A format object for encoding/decoding requests')

    def get_plural(cls):
        return cls._plural

    def set_plural(cls, value):
        cls._plural = value
    plural = property(get_plural, set_plural, None,
                      'The plural name of this object type.')

    def get_singular(cls):
        return cls._singular

    def set_singular(cls, value):
        cls._singular = value
    singular = property(get_singular, set_singular, None,
                        'The singular name of this object type.')

    def get_prefix_source(cls):
        """Return the prefix source, by default derived from site."""
        if hasattr(cls, '_prefix_source'):
            return cls._prefix_source
        else:
            return urlparse.urlsplit(cls.site)[2]

    def set_prefix_source(cls, value):
        """Set the prefix source, which will be rendered into the prefix."""
        cls._prefix_source = value
    
    prefix_source = property(get_prefix_source, set_prefix_source, None,
                             'prefix for lookups for this type of object.')

    def prefix(cls, options=None):
        """Return the rendered prefix for this object."""
        return cls._prefix(options)


class ActiveResource(object):
    """Represents an activeresource object."""

    __metaclass__ = ResourceMeta
    _connection = None
    _format = formats.XMLFormat
    _headers = None
    _password = None
    _site = None
    _timeout = None
    _user = None

    def __init__(self, attributes, prefix_options=None):
        """Initialize a new ActiveResource object.

        Args:
            attributes: A dictionary of attributes which represent this object.
            prefix_options: A dict of prefixes to add to the request for
                            nested URLs.
        """
        self.klass = self.__class__
        self.attributes = {}
        if prefix_options:
            self._prefix_options = prefix_options
        else:
            self._prefix_options = {}
        self._update(attributes)
        self.errors = Errors(self)
        self._initialized = True

    # Public class methods which act as factory functions
    @classmethod
    def find(cls, id_=None, from_=None, **kwargs):
        """Core method for finding resources.

        Args:
            id_: A specific resource to retrieve.
            from_: The path that resources will be fetched from.
            kwargs: any keyword arguments for query.

        Returns:
            An ActiveResource object.
        Raises:
            connection.Error: On any communications errors.
            Error: On any other errors.
        """
        if id_:
            return cls._find_single(id_, **kwargs)

        return cls._find_every(from_=from_, **kwargs)

    @classmethod
    def find_first(cls, from_=None, **kwargs):
        """Core method for finding resources.

        Args:
            from_: The path that resources will be fetched from.
            kwargs: any keyword arguments for query.

        Returns:
            The first resource from the list of returned resources or None if
            none are found.
        Raises:
            connection.Error: On any communications errors.
            Error: On any other errors.
        """
        resources = cls._find_every(from_=from_, **kwargs)
        if resources:
            return resources[0]

    @classmethod
    def find_one(cls, from_, **kwargs):
        """Get a single resource from a specific URL.

        Args:
            from_: The path that resources will be fetched from.
            kwargs: Any keyword arguments for query.
        Returns:
            An ActiveResource object.
        Raises:
            connection.Error: On any communications errors.
            Error: On any other errors.
        """
        return cls._find_one(from_, kwargs)

    @classmethod
    def exists(cls, id_, **kwargs):
        """Check whether a resource exists.

        Args:
            id_: The id or other key which specifies a unique object.
            kwargs: Any keyword arguments for query.
        Returns:
            True if the resource is found, False otherwise.
        """
        prefix_options, query_options = cls._split_options(kwargs)
        path = cls._element_path(id_, prefix_options, query_options)
        try:
            _ = cls.connection.head(path, cls.headers)
            return True
        except connection.Error:
            return False

    @classmethod
    def create(cls, attributes):
        """Create and save a resource with the given attributes.

        Args:
            attributes: A dictionary of attributes which represent this object.
        Returns:
            True if the resource is found, False otherwise.
        """
        resource = cls(attributes)
        resource.save()
        return resource

    # Non-public class methods to support the above
    @classmethod
    def _split_options(cls, options):
        """Split prefix options and query options.

        Args:
            options: A dictionary of prefix and/or query options.
        Returns:
            A tuple containing (prefix_options, query_options)
        """
        #TODO(mrroach): figure out prefix_options
        prefix_options = {}
        query_options = {}
        for key, value in options.items():
            if key in cls._prefix_parameters():
                prefix_options[key] = value
            else:
                query_options[key] = value
        return [prefix_options, query_options]

    @classmethod
    def _find_single(cls, id_, **kwargs):
        """Get a single object from the default URL.

        Args:
            id_: The id or other key which specifies a unique object.
            kwargs: Any keyword arguments for the query.
        Returns:
            An ActiveResource object.
        Raises:
            ConnectionError: On any error condition.
        """
        prefix_options, query_options = cls._split_options(kwargs)
        path = cls._element_path(id_, prefix_options, query_options)
        return cls._build_object(cls.connection.get(path, cls.headers),
                                 prefix_options)

    @classmethod
    def _find_one(cls, from_, query_options):
        """Find a single resource from a one-off URL.

        Args:
            from_: The path from which to retrieve the resource.
            query_options: Any keyword arguments for the query.
        Returns:
            An ActiveResource object.
        Raises:
            connection.ConnectionError: On any error condition.
        """
        #TODO(mrroach): allow from_ to be a string-generating function
        path = from_ + cls._query_string(query_options)
        return cls._build_object(cls.connection.get(path, cls.headers))

    @classmethod
    def _find_every(cls, from_=None, **kwargs):
        """Get all resources.

        Args:
            from_: (optional) The path from which to retrieve the resource.
            kwargs: Any keyword arguments for the query.
        Returns:
            A list of resources.
        """
        if from_:
            path = from_ + cls._query_string(kwargs)
            prefix_options = None
        else:
            prefix_options, query_options = cls._split_options(kwargs)
            path = cls._collection_path(prefix_options, query_options)
        return cls._build_list(cls.connection.get(path, cls.headers),
                               prefix_options)

    @classmethod
    def _build_object(cls, attributes, prefix_options=None):
        """Create an object or objects for the given resource string.

        Args:
            attributes: A dictionary representing a resource.
            prefix_options: A dict of prefixes to add to the request for
                            nested URLs.
        Returns:
            An ActiveResource object.
        """
        return cls(attributes, prefix_options)

    @classmethod
    def _build_list(cls, elements, prefix_options=None):
        """Create a list of objects for the given xml string.

        Args:
            elements: A list of dictionaries representing resources.
            prefix_options: A dict of prefixes to add to the request for
                            nested URLs.
        Returns:
            A list of ActiveResource objects.
        """
        resources = []
        for element in elements:
            resources.append(cls(element, prefix_options))
        return resources

    @classmethod
    def _query_string(cls, query_options):
        """Return a query string for the given options.

        Args:
            query_options: A dictionary of query keys/values.
        Returns:
            A string containing the encoded query.
        """
        if query_options:
            return '?' + urllib.urlencode(query_options)
        else:
            return ''

    @classmethod
    def _element_path(cls, id_, prefix_options=None, query_options=None):
        """Get the element path for the given id.

        Examples:
            Comment.element_path(1, {'post_id': 5}) -> /posts/5/act
        Args:
            id_: The id of the object to retrieve.
            prefix_options: A dict of prefixes to add to the request for
                            nested URLs.
            query_options: A dict of items to add to the query string for
                           the request.
        Returns:
            The path (relative to site) to the element formatted with the query.
        """
        return '%(prefix)s/%(plural)s/%(id)s.%(format)s%(query)s' % {
                'prefix': cls._prefix(prefix_options),
                'plural': cls._plural,
                'id': id_,
                'format': cls.format.extension,
                'query': cls._query_string(query_options)}

    @classmethod
    def _collection_path(cls, prefix_options=None, query_options=None):
        """Get the collection path for this object type.

        Examples:
            Comment.collection_path() -> /comments.xml
            Comment.collection_path(query_options={'active': 1})
                -> /comments.xml?active=1
            Comment.collection_path({'posts': 5})
                -> /posts/5/comments.xml
        Args:
            prefix_options: A dict of prefixes to add to the request for
                            nested URLs
            query_options: A dict of items to add to the query string for
                           the request.
        Returns:
            The path (relative to site) to this type of collection.
        """
        return '%(prefix)s/%(plural)s.%(format)s%(query)s' % {
                'prefix': cls._prefix(prefix_options),
                'plural': cls._plural,
                'format': cls._format.extension,
                'query': cls._query_string(query_options)}

    @classmethod
    def _custom_method_collection_url(cls, method_name, options):
        """Get the collection path for this resource type.

        Args:
            method_name: The HTTP method being used.
            options: A dictionary of query/prefix options.
        Returns:
            The path (relative to site) to this type of collection.
        """
        prefix_options, query_options = cls._split_options(options)
        path = (
            '%(prefix)s/%(plural)s/%(method_name)s.%(format)s%(query)s' %
            {'prefix': cls._prefix(prefix_options),
             'plural': cls._plural,
             'method_name': method_name,
             'format': cls.format.extension,
             'query': cls._query_string(query_options)})
        return path

    @classmethod
    def _class_get(cls, method_name, **kwargs):
        """Get a nested resource or resources.

        Args:
            method_name: the nested resource to retrieve.
            kwargs: Any keyword arguments for the query.
        Returns:
            A dictionary representing the returned data.
        """
        url = cls._custom_method_collection_url(method_name, kwargs)
        return cls.connection.get(url, cls.headers)

    @classmethod
    def _class_post(cls, method_name, body='', **kwargs):
        """Get a nested resource or resources.

        Args:
            method_name: the nested resource to retrieve.
            body: The data to send as the body of the request.
            kwargs: Any keyword arguments for the query.
        Returns:
            A connection.Response object.
        """
        url = cls._custom_method_collection_url(method_name, kwargs)
        return cls.connection.post(url, cls.headers, body)

    @classmethod
    def _class_put(cls, method_name, body='', **kwargs):
        """Get a nested resource or resources.

        Args:
            method_name: the nested resource to retrieve.
            body: The data to send as the body of the request.
            kwargs: Any keyword arguments for the query.
        Returns:
            A connection.Response object.
        """
        url = cls._custom_method_collection_url(method_name, kwargs)
        return cls.connection.put(url, cls.headers, body)

    @classmethod
    def _class_delete(cls, method_name, **kwargs):
        """Get a nested resource or resources.

        Args:
            method_name: the nested resource to retrieve.
            kwargs: Any keyword arguments for the query.
        Returns:
            A connection.Response object.
        """
        url = cls._custom_method_collection_url(method_name, kwargs)
        return cls.connection.delete(url, cls.headers)

    @classmethod
    def _prefix_parameters(cls):
        """Return a list of the parameters used in the site prefix.

        e.g. /objects/$object_id would yield ['object_id']
             /objects/${object_id}/people/$person_id/ would yield
             ['object_id', 'person_id']
        Args:
            None
        Returns:
            A set of named parameters.
        """
        path = cls.prefix_source
        template = Template(path)
        keys = set()
        for match in template.pattern.finditer(path):
            for match_type in 'braced', 'named':
                if match.groupdict()[match_type]:
                    keys.add(match.groupdict()[match_type])
        return keys

    @classmethod
    def _prefix(cls, options=None):
        """Return the prefix for this object type.

        Args:
            options: A dictionary containing additional prefixes to prepend.
        Returns:
            A string containing the path to this element.
        """
        if options is None:
            options = {}
        path = re.sub('/$', '', cls.prefix_source)
        template = Template(path)
        keys = cls._prefix_parameters()
        options = dict([(k, options.get(k, '')) for k in keys])
        return template.safe_substitute(options)

    @classmethod
    def _scrub_name(cls, name):
        """Remove invalid characters from attribute names.

        Args:
            name: the string to scrub
        Returns:
            The part of the string that is a valid name, or None if unscrubbable
        """
        name = name.lower().replace('-', '_')
        match = VALID_NAME.search(name)
        if match:
            return match.group(0)
        return None

    # Public instance methods
    def to_dict(self):
        """Convert the object to a dictionary."""
        values = {}
        for key, value in self.attributes.iteritems():
            if isinstance(value, list):
                values[key] = [i.to_dict() for i in value]
            elif isinstance(value, ActiveResource):
                values[key] = value.to_dict()
            else:
                values[key] = value
        return values

    def to_xml(self, root=None, header=True, pretty=False):
        """Convert the object to an xml string.

        Args:
            root: The name of the root element for xml output.
            header: Whether to include the xml header.
            pretty: Whether to "pretty-print" format the output.
        Returns:
            An xml string.
        """
        if not root:
            root = self._singular
        return util.to_xml(self.to_dict(), root=root,
                           header=header, pretty=pretty)

    def save(self):
        """Save the object to the server.

        Args:
            None
        Returns:
            True on success, False on ResourceInvalid errors (sets the errors
            attribute if an <errors> object is returned by the server).
        Raises:
            connection.Error: On any communications problems.
        """
        try:
            if self.id:
                response = self.klass.connection.put(
                        self._element_path(self.id, self._prefix_options),
                        self.klass.headers,
                        data=self.to_xml())
            else:
                response = self.klass.connection.post(
                        self._collection_path(self._prefix_options),
                        self.klass.headers,
                        data=self.to_xml())
                new_id = self._id_from_response(response)
                if new_id:
                    self.attributes['id'] = new_id
        except connection.ResourceInvalid, err:
            self.errors.from_xml(err.response.body)
            return False
        try:
            attributes = self.klass.format.decode(response.body)
        except formats.Error:
            return True
        if attributes:
            self._update(attributes)
        return True

    def is_valid(self):
        """Returns True if no errors have been set.

        Args:
            None
        Returns:
            True if no errors have been set, False otherwise.
        """
        return not len(self.errors)

    def _id_from_response(self, response):
        """Pull the ID out of a response from a create POST.

        Args:
            response: A Response object.
        Returns:
           An id string.
        """
        match = re.search(r'\/([^\/]*?)(\.\w+)?$',
                          response.get('Location',
                                       response.get('location', '')))
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return match.group(1)

    def destroy(self):
        """Deletes the resource from the remote service.

        Args:
            None
        Returns:
            None
        """
        self.klass.connection.delete(
                self._element_path(self.id, self._prefix_options),
                self.klass.headers)

    def __getattr__(self, name):
        """Retrieve the requested attribute if it exists.

        Args:
            name: The attribute name.
        Returns:
            The attribute's value.
        Raises:
            AttributeError: if no such attribute exists.
        """
        #TODO(mrroach): Use descriptors instead of __getattr__
        if name == 'id':
            # id should always be getattrable
            return self.attributes.get('id')
        if name in self.attributes:
            return self.attributes[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        """Set the named attributes.

        Args:
            name: The attribute name.
            value: The attribute's value.
        Returns:
            None
        """
        if '_initialized' in self.__dict__:
            if name in self.__dict__ or name in self.__class__.__dict__:
                # Update a normal attribute
                object.__setattr__(self, name, value)
            else:
                # Add/update an attribute
                self.attributes[name] = value
        object.__setattr__(self, name, value)

    def __repr__(self):
        return '%s(%s)' % (self._singular, self.id)

    def __cmp__(self, other):
        if isinstance(other, self.__class__):
            return cmp(self.id, other.id)
        else:
            return cmp(self.id, other)

    def _update(self, attributes):
        """Update the object with the given attributes.

        Args:
            attributes: A dictionary of attributes.
        Returns:
            None
        """
        if not isinstance(attributes, dict):
            return
        for key, value in attributes.items():
            if isinstance(value, dict):
                klass = self._find_class_for(key)
                attr = klass(value)
            elif isinstance(value, list):
                klass = self._find_class_for(util.singularize(key))
                attr = [klass(child) for child in value]
            else:
                attr = value
            # Store the actual value in the attributes dictionary
            self.attributes[key] = attr
            attr_name = self._scrub_name(key)

    def _find_class_for(self, element_name=None, class_name=None):
        """Look in the parent modules for classes matching the element name.

        One, or both of element/class name must be specified.

        Args:
            element_name: The name of the element type.
            class_name: The class name of the element type.
        Returns:
            A Resource class.
        """
        if not element_name and not class_name:
            raise Error('One of element_name,class_name must be specified.')
        elif not element_name:
            element_name = util.underscore(class_name)
        elif not class_name:
            class_name = util.camelize(element_name)

        module_path = self.__module__.split('.')
        for depth in range(len(module_path), 0, -1):
            try:
                __import__('.'.join(module_path[:depth]))
                module = sys.modules['.'.join(module_path[:depth])]
            except ImportError:
                continue
            try:
                klass = getattr(module, class_name)
                return klass
            except AttributeError:
                try:
                    __import__('.'.join([module.__name__, element_name]))
                    submodule = sys.modules['.'.join([module.__name__,
                                                      element_name])]
                except ImportError:
                    continue
                try:
                    klass = getattr(submodule, class_name)
                    return klass
                except AttributeError:
                    continue

        # If we made it this far, no such class was found
        return new.classobj(class_name, (self.__class__,),
                            {'__module__': self.__module__})

    # methods corresponding to Ruby's custom_methods
    def _custom_method_element_url(self, method_name, options):
        """Get the element path for this type of object.

        Args:
            method_name: The HTTP method being used.
            options: A dictionary of query/prefix options.
        Returns:
            The path (relative to site) to the element formatted with the query.
        """
        prefix_options, query_options = self._split_options(options)
        prefix_options.update(self._prefix_options)
        path = (
            '%(prefix)s/%(plural)s/%(id)s/%(method_name)s.%(format)s%(query)s' %
            {'prefix': self.klass.prefix(prefix_options),
             'plural': self._plural,
             'id': self.id,
             'method_name': method_name,
             'format': self._format.extension,
             'query': self._query_string(query_options)})
        return path

    def _custom_method_new_element_url(self, method_name, options):
        """Get the element path for creating new objects of this type.

        Args:
            method_name: The HTTP method being used.
            options: A dictionary of query/prefix options.
        Returns:
            The path (relative to site) to the element formatted with the query.
        """
        prefix_options, query_options = self._split_options(options)
        prefix_options.update(self._prefix_options)
        path = (
            '%(prefix)s/%(plural)s/new/%(method_name)s.%(format)s%(query)s' %
            {'prefix': self.klass.prefix(prefix_options),
             'plural': self._plural,
             'method_name': method_name,
             'format': self._format.extension,
             'query': self._query_string(query_options)})
        return path

    def _instance_get(self, method_name, **kwargs):
        """Get a nested resource or resources.

        Args:
            method_name: the nested resource to retrieve.
            kwargs: Any keyword arguments for the query.
        Returns:
            A dictionary representing the returned data.
        """
        url = self._custom_method_element_url(method_name, kwargs)
        return self.klass.connection.get(url, self.klass.headers)

    def _instance_post(self, method_name, body='', **kwargs):
        """Create a new resource/nested resource.

        Args:
            method_name: the nested resource to post to.
            body: The data to send as the body of the request.
            kwargs: Any keyword arguments for the query.
        Returns:
            A connection.Response object.
        """
        if self.id:
            url = self._custom_method_element_url(method_name, kwargs)
        else:
            if not body:
                body = self.to_xml()
            url = self._custom_method_new_element_url(method_name, kwargs)
        return self.klass.connection.post(url, self.klass.headers, body)

    def _instance_put(self, method_name, body='', **kwargs):
        """Update a nested resource.

        Args:
            method_name: the nested resource to update.
            body: The data to send as the body of the request.
            kwargs: Any keyword arguments for the query.
        Returns:
            A connection.Response object.
        """
        url = self._custom_method_element_url(method_name, kwargs)
        return self.klass.connection.put(url, self.klass.headers, body)

    def _instance_delete(self, method_name, **kwargs):
        """Get a nested resource or resources.

        Args:
            method_name: the nested resource to retrieve.
            kwargs: Any keyword arguments for the query.
        Returns:
            A connection.Response object.
        """
        url = self._custom_method_element_url(method_name, kwargs)
        return self.klass.connection.delete(url, self.klass.headers)

    # Create property which returns class/instance method based on context
    get = ClassAndInstanceMethod('_class_get', '_instance_get')
    post = ClassAndInstanceMethod('_class_post', '_instance_post')
    put = ClassAndInstanceMethod('_class_put', '_instance_put')
    delete = ClassAndInstanceMethod('_class_delete', '_instance_delete')
