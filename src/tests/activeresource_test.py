#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Tests for ActiveResource objects."""

__author__ = 'Mark Roach (mrroach@google.com)'
import unittest
from pyactiveresource import activeresource
from pyactiveresource import fake_connection
from pyactiveresource import util


class ActiveResourceTest(unittest.TestCase):
    def setUp(self):
        """Create test objects."""
        self.arnold = {'id': 1, 'name': 'Arnold Ziffel'}
        self.eb = {'id': 2, 'name': 'Eb Dawson'}
        self.sam = {'id': 3, 'name': 'Sam Drucker'}
        self.soup = {'id': 1, 'name': 'Hot Water Soup'}
        self.store_new = {'name': 'General Store'}
        self.store = {'id': 1, 'name': 'General Store'}
        self.store_update = {'manager_id': 3, 'id': 1, 'name':'General Store'}

    def test_find_one(self):
        """Test the find_one method."""
        connection = fake_connection.FakeConnection()
        # Return an object for a specific one-off url
        connection.respond_to(
            'get', '/what_kind_of_soup.xml', None, None,
            util.to_xml(self.soup, root='soup'))

        class Soup(activeresource.ActiveResource):
            _connection_obj = connection        
        soup = Soup.find_one(from_='/what_kind_of_soup.xml')
        self.assertEqual(self.soup, soup.attributes)

    def test_find(self):
        """Test the find method."""
        connection = fake_connection.FakeConnection()
        # Return a list of people for a find method call
        connection.respond_to(
            'get', '/people.xml', None, None,
            util.to_xml([self.arnold, self.eb], root='people'))
        
        class Person(activeresource.ActiveResource):
            _connection_obj = connection
        people = Person.find()
        self.assertEqual([self.arnold, self.eb],
                         [p.attributes for p in people])

    def test_find_by_id(self):
        """Test the find method when called with an id argument."""
        connection = fake_connection.FakeConnection()
        # Return a single person for a find(id=<id>) call
        connection.respond_to(
            'get', '/people/1.xml', None, None,
            util.to_xml(self.arnold, root='person'))

        class Person(activeresource.ActiveResource):
            _connection_obj = connection
        
        arnold = Person.find(1)
        self.assertEqual(self.arnold, arnold.attributes)
    
    def test_find_with_options(self):
        """Test the find method when called with prefix/query options."""
        connection = fake_connection.FakeConnection()
        # Return a single-item people list for a find() call with kwargs
        connection.respond_to(
            'get', '/people.xml?name=Arnold', None, None,
            util.to_xml([self.arnold], root='people'))
        # Paths for prefix_options related requests
        connection.respond_to(
            'get', '/stores/1/people.xml', None, None,
            util.to_xml([self.sam], root='people'))
        connection.respond_to(
            'get', '/stores/1/people.xml?name=Ralph', None, None,
            util.to_xml([], root='people'))
        
        class Person(activeresource.ActiveResource):
            _connection_obj = connection
            
        # Query options only
        arnold = Person.find(name='Arnold')[0]
        self.assertEqual(self.arnold, arnold.attributes)
        
        # Prefix options only
        Person._site = 'http://localhost/stores/$store_id/'
        sam = Person.find(store_id=1)[0]
        self.assertEqual(self.sam, sam.attributes)
        
        # Query & prefix options
        nobody = Person.find(store_id=1, name='Ralph')
        self.assertEqual([], nobody)

    def test_save(self):
        """Test objection creation and saving."""
        connection = fake_connection.FakeConnection()
        # Return an object with id for a post(save) request.
        connection.respond_to(
            'post', '/stores.xml', None,
            util.to_xml(self.store_new, root='store'),
            util.to_xml(self.store))
        # Return an object for a put request.
        connection.respond_to(
            'put', '/stores/1.xml', None,
            util.to_xml(self.store_update, root='store'),
            util.to_xml(self.store_update, root='store'))
        class Store(activeresource.ActiveResource):
            _connection_obj = connection
        
        store = Store(self.store_new)
        store.save()
        self.assertEqual(self.store, store.attributes)
        store.manager_id = 3
        store.save()


if __name__ == '__main__':
    unittest.main()
