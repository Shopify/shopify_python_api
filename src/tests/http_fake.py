#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Fake urllib2 HTTP connection objects."""

__author__ = 'Mark Roach (mrroach@google.com)'


import urllib2
import urlparse
from StringIO import StringIO
from pprint import pformat


class Error(Exception):
    """Base exception type for this module."""


def initialize():
    """Install TestHandler as the only active handler for http requests."""
    opener = urllib2.build_opener(TestHandler)
    urllib2.install_opener(opener)


class TestHandler(urllib2.HTTPHandler, urllib2.HTTPSHandler):
    """A urllib2 handler object which returns a predefined response."""

    _response = None
    _response_map = {}
    request = None
    site = ''

    @classmethod
    def set_response(cls, response):
        """Set a static response to be returned for all requests.
        
        Args:
            response: A FakeResponse object to be returned.
        """
        cls._response_map = {}
        cls._response = response

    @classmethod
    def respond_to(cls, method, path,
                   request_headers, body, code=200, response_headers=None):
        """Build a response object to be used for a specific request.
        
        Args:
            method: The http method (e.g. 'get', 'put' etc.)
            path: The path being requested (e.g. '/collection/id.xml')
            request_headers: Dictionary of headers passed along with the request
            body: The string that should be returned for a matching request
            code: The http response code to return
            response_headers: Dictionary of headers to return
        Returns:
            None
        """
        key = (method, urlparse.urljoin(cls.site, path), request_headers)
        value = (code, body, response_headers)
        cls._response_map[str(key)] = value

    def do_open(self, http_class, request):
        """Return the response object for the given request.
        
        Overrides the HTTPHandler method of the same name to return a
        FakeResponse instead of creating any network connections.
        
        Args:
            http_class: The http protocol being used.
            request: A urllib2.Request object.
        Returns:
            A FakeResponse object.
        """
        self.__class__.request = request  # Store the most recent request object
        if self._response_map:
            key = (request.get_method(),
                   request.get_full_url(),
                   request.headers)
            if str(key) in self._response_map:
                (code, body, response_headers) = self._response_map[str(key)]
                return FakeResponse(code, body, response_headers) 
            else:
                raise Error('Unknown request %s %s'
                            '\nrequest:%s\nresponse_map:%s' % (
                            request.get_method(), request.get_full_url(),
                            str(key), pformat(self._response_map.keys())))
        elif isinstance(self._response, Exception):
            raise(self._response)
        else:
            return self._response


class FakeResponse(object):
    '''A fake HTTPResponse object for testing.'''
    
    def __init__(self, code, body, headers=None):
        self.code = code
        self.msg = str(code)
        if headers is None:
            headers = {}
        self.headers = headers
        self.info = lambda: self.headers
        self.body_file = StringIO(body)
    
    def read(self):
        """Read the entire response body."""
        return self.body_file.read()
    
    def readline(self):
        """Read a single line from the response body."""
        return self.body_file.readline()
