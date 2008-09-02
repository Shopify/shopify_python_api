#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Tests for util functions."""

__author__ = 'Mark Roach (mrroach@google.com)'

import datetime
import decimal
import unittest
from pyactiveresource import util
from pprint import pprint


def diff_dicts(d1, d2):
    """Print the differences between two dicts. Useful for troubleshooting."""
    pprint([(k,v) for k,v in d2.items()
            if v != d1[k]])


class UtilTest(unittest.TestCase):
    def setUp(self):
        """Create test objects."""

    def test_xml_to_dict_single_record(self):
        """Test the xml_to_dict function."""
        topic_xml = '''<topic>
             <title>The First Topic</title>
             <author-name>David</author-name>
             <id type="integer">1</id>
             <approved type="boolean"> true </approved>
             <replies-count type="integer">0</replies-count>
             <replies-close-in type="integer">2592000000</replies-close-in>
             <written-on type="date">2003-07-16</written-on>
             <viewed-at type="datetime">2003-07-16T09:28:00+0000</viewed-at>
             <content type="yaml">--- \n1: should be an integer\n:message: Have a nice day\narray: \n- should-have-dashes: true\n  should_have_underscores: true\n</content>
             <author-email-address>david@loudthinking.com</author-email-address>
             <parent-id></parent-id>
             <ad-revenue type="decimal">1.5</ad-revenue>
             <optimum-viewing-angle type="float">135</optimum-viewing-angle>
             <resident type="symbol">yes</resident>
           </topic>'''

        expected_topic_dict = {
            'title': 'The First Topic',
            'author_name': 'David',
            'id': 1,
            'approved': True,
            'replies_count': 0,
            'replies_close_in': 2592000000L,
            'written_on': datetime.date(2003, 7, 16),
            'viewed_at': datetime.datetime(2003, 7, 16, 9, 28),
            'content': {':message': 'Have a nice day',
                        1: 'should be an integer',
                        'array': [{'should-have-dashes': True,
                                   'should_have_underscores': True}]},
            'author_email_address': 'david@loudthinking.com',
            'parent_id': None,
            'ad_revenue': decimal.Decimal('1.5'),
            'optimum_viewing_angle': 135.0,
            'resident': 'yes'}

        self.assertEqual(expected_topic_dict, util.xml_to_dict(topic_xml))
        self.assertEqual(expected_topic_dict,
                         util.xml_to_dict(topic_xml, saveroot=True)['topic'])

    def test_xml_to_dict_multiple_records(self):
        """Test the xml to dict function."""
        topics_xml = '''<topics type="array">
            <topic>
              <title>The First Topic</title>
              <author-name>David</author-name>
              <id type="integer">1</id>
              <approved type="boolean">false</approved>
              <replies-count type="integer">0</replies-count>
              <replies-close-in type="integer">2592000000</replies-close-in>
              <written-on type="date">2003-07-16</written-on>
              <viewed-at type="datetime">2003-07-16T09:28:00+0000</viewed-at>
              <content>Have a nice day</content>
              <author-email-address>david@loudthinking.com</author-email-address>
              <parent-id nil="true"></parent-id>
            </topic>
            <topic>
              <title>The Second Topic</title>
              <author-name>Jason</author-name>
              <id type="integer">1</id>
              <approved type="boolean">false</approved>
              <replies-count type="integer">0</replies-count>
              <replies-close-in type="integer">2592000000</replies-close-in>
              <written-on type="date">2003-07-16</written-on>
              <viewed-at type="datetime">2003-07-16T09:28:00+0000</viewed-at>
              <content>Have a nice day</content>
              <author-email-address>david@loudthinking.com</author-email-address>
              <parent-id></parent-id>
            </topic>
          </topics>'''

        expected_topic_dict = {
          'title': 'The First Topic',
          'author_name': 'David',
          'id': 1,
          'approved': False,
          'replies_count': 0,
          'replies_close_in': 2592000000L,
          'written_on': datetime.date(2003, 7, 16),
          'viewed_at': datetime.datetime(2003, 7, 16, 9, 28),
          'content': 'Have a nice day',
          'author_email_address': 'david@loudthinking.com',
          'parent_id': None}

        self.assertEqual(expected_topic_dict,
                         util.xml_to_dict(topics_xml)[0])
        self.assertEqual(
                expected_topic_dict,
                util.xml_to_dict(topics_xml, saveroot=True)['topics'][0])

    def test_xml_to_dict_empty_array(self):
        blog_xml = '''<blog>
            <posts type="array"></posts>
            </blog>'''
        expected_blog_dict = {'blog': {'posts': []}}
        self.assertEqual(expected_blog_dict,
                         util.xml_to_dict(blog_xml, saveroot=True))

    def test_xml_to_dict_empty_array_with_whitespace(self):
        blog_xml = '''<blog>
            <posts type="array">
            </posts>
          </blog>'''
        expected_blog_dict = {'blog': {'posts': []}}
        self.assertEqual(expected_blog_dict,
                         util.xml_to_dict(blog_xml, saveroot=True))

    def test_xml_to_dict_array_with_one_entry(self):
        blog_xml = '''<blog>
            <posts type="array">
              <post>a post</post>
            </posts>
          </blog>'''
        expected_blog_dict = {'blog': {'posts': ['a post']}}
        self.assertEqual(expected_blog_dict,
                         util.xml_to_dict(blog_xml, saveroot=True))

    def test_xml_to_dict_file(self):
        blog_xml = '''<blog>
            <logo type="file" name="logo.png" content_type="image/png">
            </logo>
          </blog>'''
        blog_dict = util.xml_to_dict(blog_xml, saveroot=True)
        self.assert_('blog' in blog_dict)
        self.assert_('logo' in blog_dict['blog'])
        blog_file = blog_dict['blog']['logo']
        self.assertEqual('logo.png', blog_file.name)
        self.assertEqual('image/png', blog_file.content_type)


    def test_xml_to_dict_file_with_defaults(self):
        blog_xml = '''<blog>
            <logo type="file">
            </logo>
          </blog>'''
        blog_dict = util.xml_to_dict(blog_xml, saveroot=True)
        self.assert_('blog' in blog_dict)
        self.assert_('logo' in blog_dict['blog'])
        blog_file = blog_dict['blog']['logo']
        self.assertEqual('untitled', blog_file.name)
        self.assertEqual('application/octet-stream', blog_file.content_type)

    def test_xml_to_dict_xsd_like_types(self):
        bacon_xml = '''<bacon>
            <weight type="double">0.5</weight>
            <price type="decimal">12.50</price>
            <chunky type="boolean"> 1 </chunky>
            <expires-at type="dateTime">2007-12-25T12:34:56+0000</expires-at>
            <notes type="string"></notes>
            <illustration type="base64Binary">YmFiZS5wbmc=</illustration>
            </bacon>'''
        expected_bacon_dict = {
            'weight': 0.5,
            'chunky': True,
            'price': decimal.Decimal('12.50'),
            'expires_at': datetime.datetime(2007, 12, 25, 12, 34, 56),
            'notes': '',
            'illustration': 'babe.png'}

        diff_dicts(expected_bacon_dict,
                         util.xml_to_dict(bacon_xml, saveroot=True)['bacon'])

    def test_xml_to_dict_unknown_type(self):
        product_xml = '''<product>
            <weight type="double">0.5</weight>
            <image type="ProductImage"><filename>image.gif</filename></image>
           </product>'''
        expected_product_dict = {
            'weight': 0.5,
            'image': {'type': 'ProductImage', 'filename': 'image.gif'}}
        self.assertEqual(
                expected_product_dict,
                util.xml_to_dict(product_xml, saveroot=True)['product'])


if __name__ == '__main__':
    unittest.main()
