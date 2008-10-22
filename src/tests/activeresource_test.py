#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Tests for ActiveResource objects."""

__author__ = 'Mark Roach (mrroach@google.com)'

import unittest
from pyactiveresource import activeresource
from pyactiveresource import connection
from pyactiveresource import util
from pyactiveresource.tests import http_fake


class Error(Exception):
    pass


class ActiveResourceTest(unittest.TestCase):
    """Tests for activeresource.ActiveResource."""

    def setUp(self):
        """Create test objects."""
        self.arnold = {'id': 1, 'name': 'Arnold Ziffel'}
        self.eb = {'id': 2, 'name': 'Eb Dawson'}
        self.sam = {'id': 3, 'name': 'Sam Drucker'}
        self.soup = {'id': 1, 'name': 'Hot Water Soup'}
        self.store_new = {'name': 'General Store'}
        self.general_store = {'id': 1, 'name': 'General Store'}
        self.store_update = {'manager_id': 3, 'id': 1, 'name':'General Store'}
        self.xml_headers = {'Content-type': 'application/xml'}

        self.matz  = util.to_xml(
                {'id': 1, 'name': 'Matz'}, root='person')
        self.matz_deep  = util.to_xml(
                {'id': 1, 'name': 'Matz', 'other': 'other'},
                root='person')
        self.matz_array = util.to_xml(
                [{'id': 1, 'name': 'Matz'}], root='people')
        self.ryan = util.to_xml(
                {'name': 'Ryan'}, root='person')
        self.addy = util.to_xml(
                {'id': 1, 'street': '12345 Street'},
                root='address')
        self.addy_deep  = util.to_xml(
                {'id': 1, 'street': '12345 Street', 'zip': "27519" },
                root='address')

        http_fake.initialize()  # Fake all http requests
        self.http = http_fake.TestHandler
        self.http.set_response(Error('Bad request'))
        self.http.site = 'http://localhost'

        class Person(activeresource.ActiveResource):
            _site = 'http://localhost'
        self.person = Person

        class Store(activeresource.ActiveResource):
            _site = 'http://localhost'
        self.store = Store

        class Address(activeresource.ActiveResource):
            _site = 'http://localhost/people/$person_id/'
        self.address = Address

    def test_find_one(self):
        # Return an object for a specific one-off url
        self.http.respond_to(
            'GET', '/what_kind_of_soup.xml', {},
            util.to_xml(self.soup, root='soup'))

        class Soup(activeresource.ActiveResource):
            _site = 'http://localhost'
        soup = Soup.find_one(from_='/what_kind_of_soup.xml')
        self.assertEqual(self.soup, soup.attributes)

    def test_find(self):
        # Return a list of people for a find method call
        self.http.respond_to(
            'GET', '/people.xml', {},
            util.to_xml([self.arnold, self.eb], root='people'))

        people = self.person.find()
        self.assertEqual([self.arnold, self.eb],
                         [p.attributes for p in people])

    def test_find_parses_non_array_collection(self):
        collection_xml = '''<people>
                <person><name>bob</name><id>1</id></person>
                <person><name>jim</name><id>2</id></person>
              </people>'''
        self.http.respond_to('GET', '/people.xml', {}, collection_xml)
        self.assertRaises(Exception, self.person.find)

    def test_find_parses_single_item_non_array_collection(self):
        collection_xml = '''<people>
                <person><name>jim</name><id>2</id></person>
              </people>'''
        self.http.respond_to('GET', '/people.xml', {}, collection_xml)
        self.assertRaises(Exception, self.person.find)

    def test_find_by_id(self):
        # Return a single person for a find(id=<id>) call
        self.http.respond_to(
            'GET', '/people/1.xml', {}, util.to_xml(self.arnold, root='person'))

        arnold = self.person.find(1)
        self.assertEqual(self.arnold, arnold.attributes)

    def test_find_with_query_options(self):
        # Return a single-item people list for a find() call with kwargs
        self.http.respond_to(
            'GET', '/people.xml?name=Arnold', {},
            util.to_xml([self.arnold], root='people'))
        # Query options only
        arnold = self.person.find(name='Arnold')[0]
        self.assertEqual(self.arnold, arnold.attributes)

    def test_find_with_prefix_options(self):
        # Paths for prefix_options related requests
        self.http.respond_to(
            'GET', '/stores/1/people.xml', {},
            util.to_xml([self.sam], root='people'))
        # Prefix options only
        self.person._site = 'http://localhost/stores/$store_id/'
        sam = self.person.find(store_id=1)[0]
        self.assertEqual(self.sam, sam.attributes)

    def test_find_with_prefix_and_query_options(self):
        self.http.respond_to(
            'GET', '/stores/1/people.xml?name=Ralph', {},
            util.to_xml([], root='people'))
        # Query & prefix options
        self.person._site = 'http://localhost/stores/$store_id/'
        nobody = self.person.find(store_id=1, name='Ralph')
        self.assertEqual([], nobody)

    def test_set_prefix_source(self):
      self.http.respond_to(
          'GET', '/stores/1/people.xml?name=Ralph', {},
          util.to_xml([], root='people'))
      self.person.prefix_source = '/stores/${store_id}/'
      nobody = self.person.find(store_id=1, name='Ralph')
      self.assertEqual([], nobody)

    def test_save(self):
        # Return an object with id for a post(save) request.
        self.http.respond_to(
            'POST', '/stores.xml', self.xml_headers,
            util.to_xml(self.general_store))
        # Return an object for a put request.
        self.http.respond_to(
            'PUT', '/stores/1.xml', self.xml_headers,
            util.to_xml(self.store_update, root='store'))

        store = self.store(self.store_new)
        store.save()
        self.assertEqual(self.general_store, store.attributes)
        store.manager_id = 3
        store.save()

    def test_class_get(self):
        self.http.respond_to('GET', '/people/retrieve.xml?name=Matz',
                             {}, self.matz_array)
        self.assertEqual([{'id': 1, 'name': 'Matz'}],
                         self.person.get('retrieve', name='Matz' ))

    def test_class_post(self):
        self.http.respond_to('POST', '/people/hire.xml?name=Matz', {}, '')
        self.assertEqual(connection.Response(200, ''),
                         self.person.post('hire', name='Matz'))

    def test_class_put(self):
        self.http.respond_to('PUT', '/people/promote.xml?name=Matz',
                             self.xml_headers, '')
        self.assertEqual(connection.Response(200, ''),
                         self.person.put('promote', 'atestbody', name='Matz'))

    def test_class_put_nested(self):
        self.http.respond_to('PUT', '/people/1/addresses/sort.xml?by=name',
                             {}, '')
        self.assertEqual(connection.Response(200, ''),
                         self.address.put('sort', person_id=1, by='name'))

    def test_class_delete(self):
        self.http.respond_to('DELETE', '/people/deactivate.xml?name=Matz',
                             {}, '')
        self.assertEqual(connection.Response(200, ''),
                         self.person.delete('deactivate', name='Matz'))

    def test_instance_get(self):
        self.http.respond_to('GET', '/people/1.xml', {}, self.matz)
        self.http.respond_to('GET', '/people/1/shallow.xml', {}, self.matz)
        self.assertEqual({'id': 1, 'name': 'Matz'},
                         self.person.find(1).get('shallow'))
        self.http.respond_to('GET', '/people/1/deep.xml', {}, self.matz_deep)
        self.assertEqual({'id': 1, 'name': 'Matz', 'other': 'other'},
                         self.person.find(1).get('deep'))

    def test_instance_post_new(self):
        ryan = self.person({'name': 'Ryan'})
        self.http.respond_to('POST', '/people/new/register.xml',
                             self.xml_headers, '')
        self.assertEqual(
            connection.Response(200, ''), ryan.post('register'))

    def test_instance_post(self):
        self.http.respond_to('POST', '/people/1/register.xml', {}, self.matz)
        matz = self.person({'id': 1, 'name': 'Matz'})
        self.assertEqual(connection.Response(200, self.matz),
                         matz.post('register'))

    def test_instance_put(self):
        self.http.respond_to('GET', '/people/1.xml', {}, self.matz)
        self.http.respond_to(
            'PUT', '/people/1/promote.xml?position=Manager',
            self.xml_headers, '')
        self.assertEqual(
            connection.Response(200, ''),
            self.person.find(1).put('promote', 'body', position='Manager'))

    def test_instance_put_nested(self):
        self.http.respond_to(
            'GET', '/people/1/addresses/1.xml', {}, self.addy)
        self.http.respond_to(
            'PUT', '/people/1/addresses/1/normalize_phone.xml?locale=US',
            {}, '', 204)

        self.assertEqual(
            connection.Response(204, ''),
            self.address.find(1, person_id=1).put('normalize_phone',
                                                  locale='US'))

    def test_instance_get_nested(self):
        self.http.respond_to(
            'GET', '/people/1/addresses/1.xml', {}, self.addy)
        self.http.respond_to(
            'GET', '/people/1/addresses/1/deep.xml', {}, self.addy_deep)
        self.assertEqual({'id': 1, 'street': '12345 Street', 'zip': "27519" },
                         self.address.find(1, person_id=1).get('deep'))


    def test_instance_delete(self):
        self.http.respond_to('GET', '/people/1.xml', {}, self.matz)
        self.http.respond_to('DELETE', '/people/1/deactivate.xml', {}, '')
        self.assertEqual('', self.person.find(1).delete('deactivate').body)

    def test_should_accept_setting_user(self):
        self.person.user = 'david'
        self.assertEqual('david', self.person.user)
        self.assertEqual('david', self.person.connection.user)

    def test_should_accept_setting_password(self):
        self.person.password = 'test123'
        self.assertEqual('test123', self.person.password)
        self.assertEqual('test123', self.person.connection.password)

    def test_should_accept_setting_timeout(self):
        self.person.timeout = 77
        self.assertEqual(77, self.person.timeout)
        self.assertEqual(77, self.person.connection.timeout)

    def test_user_variable_can_be_reset(self):
        class Actor(activeresource.ActiveResource): pass
        Actor.site = 'http://cinema'
        self.assert_(Actor.user is None)
        Actor.user = 'username'
        Actor.user = None
        self.assert_(Actor.user is None)
        self.assert_(Actor.connection.user is None)

    def test_password_variable_can_be_reset(self):
        class Actor(activeresource.ActiveResource): pass
        Actor.site = 'http://cinema'
        self.assert_(Actor.password is None)
        Actor.password = 'password'
        Actor.password = None
        self.assert_(Actor.password is None)
        self.assert_(Actor.connection.password is None)

    def test_timeout_variable_can_be_reset(self):
        class Actor(activeresource.ActiveResource): pass
        Actor.site = 'http://cinema'
        self.assert_(Actor.timeout is None)
        Actor.timeout = 5
        Actor.timeout = None
        self.assert_(Actor.timeout is None)
        self.assert_(Actor.connection.timeout is None)

    def test_credentials_from_site_are_decoded(self):
        class Actor(activeresource.ActiveResource): pass
        Actor.site = 'http://my%40email.com:%31%32%33@cinema'
        self.assertEqual('my@email.com', Actor.user)
        self.assertEqual('123', Actor.password)

    def test_site_attribute_declaration_is_parsed(self):
        class Actor(activeresource.ActiveResource):
            _site = 'http://david:test123@localhost.localsite:4000/api'
        self.assertEqual(['david', 'test123'], [Actor.user, Actor.password])

    def test_changing_subclass_site_does_not_affect_superclass(self):
        class Actor(self.person): pass

        Actor.site = 'http://actor-site'
        self.assertNotEqual(Actor.site, self.person.site)

    def test_changing_superclass_site_affects_unset_subclass_site(self):
        class Actor(self.person): pass

        self.person.site = 'http://person-site'
        self.assertEqual(Actor.site, self.person.site)

    def test_changing_superclass_site_does_not_affect_set_subclass_set(self):
        class Actor(self.person): pass

        Actor.site = 'http://actor-site'
        self.person.site = 'http://person-site'
        self.assertNotEqual(Actor.site, self.person.site)

    def test_updating_superclass_site_resets_descendent_connection(self):
        class Actor(self.person): pass
        
        self.assert_(self.person.connection is Actor.connection)
        
        self.person.site = 'http://another-site'
        self.assert_(self.person.connection is Actor.connection)
    
    def test_updating_superclass_user_resets_descendent_connection(self):
        class Actor(self.person): pass
        
        self.assert_(self.person.connection is Actor.connection)
        
        self.person.user = 'username'
        self.assert_(self.person.connection is Actor.connection)
    
    def test_updating_superclass_password_resets_descendent_connection(self):
        class Actor(self.person): pass
        
        self.assert_(self.person.connection is Actor.connection)
        
        self.person.password = 'password'
        self.assert_(self.person.connection is Actor.connection)

    def test_updating_superclass_timeout_resets_descendent_connection(self):
        class Actor(self.person): pass
        
        self.assert_(self.person.connection is Actor.connection)
        
        self.person.timeout = 10
        self.assert_(self.person.connection is Actor.connection)


if __name__ == '__main__':
    unittest.main()
