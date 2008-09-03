#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""A fake HTTP connection for testing"""

__author__ = 'Mark Roach (mrroach@google.com)'

import re
import urllib
import urlparse

class Error(Exception):
    """The base exception class for this module."""


class FakeConnection(object):
    """A fake HTTP connection for testing.
    
    Inspired by ActiveResource's HttpMock class. This class is designed to
    take a list of inputs and their corresponding outputs.
    
    Inputs will be matched on the method, path, query and data arguments
    
    Example:
    >>> connection = FakeConnection()
    >>> body = '<?xml ... />'
    >>> connection.respond_to('get', '/foos/1.xml', None, None, body)
    >>> class Foo(resource.Resource):
    ...     _site = 'http://localhost/'
    ...
    >>> Foo._connection_obj = connection
    >>> Foo.find(1)
    foo(1)
    """
    def __init__(self):
        """Constructor for FakeConnection object."""
        self._request_map = {}

    def _split_path(self, path):
        """Return the path and the query string as a dictionary."""
        path_only, query_string = urllib.splitquery(path)
        if query_string:
            query_dict = dict([i.split('=') for i in query_string.split('&')])
        else:
            query_dict = {}
        return path_only, query_dict

    def debug_only(self, debug=True):
        self._debug_only = debug

    def respond_to(self, method, path, headers, data, body):
        """Set the response for a given request.
        
        Args:
            method: The http method (e.g. 'get', 'put' etc.).
            path: The path being requested (e.g. '/collection/id.xml')
            headers: Dictionary of headers passed along with the request.
            data: The data being passed in as the request body.
            body: The string that should be returned for a matching request.
        Returns:
            None
        """
        path_only, query = self._split_path(path)
        self._request_map.setdefault(method, []).append(
                ((path_only, query, headers, data), body))

    def _lookup_response(self, method, path, headers, data):
        path_only, query = self._split_path(path)
        for key, value in self._request_map.get(method, {}):
            if key == (path_only, query, headers, data):
                return value
        raise Error('Invalid or unknown request: %s %s\n%s' %
                    (path, headers, data))
        
    def get(self, path, headers=None):
        """Perform an HTTP get request."""
        return self._lookup_response('get', path, headers, None)
        
    def post(self, path, headers=None, data=None):
        """Perform an HTTP post request."""
        return self._lookup_response('post', path, headers, data)
    
    def put(self, path, headers=None, data=None):
        """Perform an HTTP post request."""
        return self._lookup_response('put', path, headers, data)
    
    def delete(self, path, headers=None):
        """Perform an HTTP delete request."""
        return self._lookup_response('delete', path, headers, None)
