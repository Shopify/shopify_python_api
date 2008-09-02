#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Tests for util functions."""

__author__ = 'Mark Roach (mrroach@google.com)'

import datetime
import unittest
from pyactiveresource import util


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
            'replies_close_in': 2592000000,
            'written_on': datetime.date(2003, 7, 16),
            'viewed_at': datetime.datetime(2003, 7, 16, 9, 28),
            'content': {'message': 'Have a nice day',
                        1: 'should be an integer',
                        'array': [{'should-have-dashes': True,
                                   'should_have_underscores': True}]},
            'author_email_address': 'david@loudthinking.com',
            'parent_id': None,
            'ad_revenue': 1.5,
            'optimum_viewing_angle': 135.0,
            'resident': 'yes'}
        self.assertEqual(expected_topic_dict, util.xml_to_dict(topic_xml))


if __name__ == '__main__':
    unittest.main()
