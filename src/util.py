#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Utilities for pyActiveResource."""

__author__ = 'Mark Roach (mrroach@google.com)'

import base64
import calendar
import decimal
import re
import time
import datetime
try:
    import yaml
except ImportError:
    yaml = None

try:
    from dateutil.parser import parse as date_parse
except ImportError:
    try:
        from xml.utils import iso8601
        def date_parse(time_string):
            """Return a datetime object for the given ISO8601 string.
            
            Args:
                time_string: An ISO8601 timestamp.
            Returns:
                A datetime.datetime object.
            """
            return datetime.datetime.utcfromtimestamp(
                    iso8601.parse(time_string))
    except ImportError:
        date_parse = None

try:
    from xml.etree import cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        try:
            from xml.etree import ElementTree as ET
        except ImportError:
            from elementtree import ElementTree as ET

XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>'

# Patterns blatently stolen from Rails' Inflector
PLURALIZE_PATTERNS = [
    (r'(quiz)$', r'\1zes'),
    (r'^(ox)$', r'\1en'),
    (r'([m|l])ouse$', r'\1ice'),
    (r'(matr|vert|ind)(?:ix|ex)$', r'\1ices'),
    (r'(x|ch|ss|sh)$', r'\1es'),
    (r'([^aeiouy]|qu)y$', r'\1ies'),
    (r'(hive)$', r'1s'),
    (r'(?:([^f])fe|([lr])f)$', r'\1\2ves'),
    (r'sis$', r'ses'),
    (r'([ti])um$', r'\1a'),
    (r'(buffal|tomat)o$', r'\1oes'),
    (r'(bu)s$', r'\1ses'),
    (r'(alias|status)$', r'\1es'),
    (r'(octop|vir)us$', r'\1i'),
    (r'(ax|test)is$', r'\1es'),
    (r's$', 's'),
    (r'$', 's')
]

SINGULARIZE_PATTERNS = [
    (r'(quiz)zes$', r'1'),
    (r'(matr)ices$', r'1ix'),
    (r'(vert|ind)ices$', r'1ex'),
    (r'^(ox)en', r'1'),
    (r'(alias|status)es$', r'1'),
    (r'(octop|vir)i$', r'1us'),
    (r'(cris|ax|test)es$', r'1is'),
    (r'(shoe)s$', r'1'),
    (r'(o)es$', r'1'),
    (r'(bus)es$', r'1'),
    (r'([m|l])ice$', r'1ouse'),
    (r'(x|ch|ss|sh)es$', r'1'),
    (r'(m)ovies$', r'1ovie'),
    (r'(s)eries$', r'1eries'),
    (r'([^aeiouy]|qu)ies$', r'1y'),
    (r'([lr])ves$', r'1f'),
    (r'(tive)s$', r'1'),
    (r'(hive)s$', r'1'),
    (r'([^f])ves$', r'1fe'),
    (r'(^analy)ses$', r'1sis'),
    (r'((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)ses$',
     r'12sis'),
    (r'([ti])a$', r'1um'),
    (r'(n)ews$', r'1ews'),
    (r's$', r'')
]

IRREGULAR = [
    ('person', 'people'),
    ('man', 'men'),
    ('child', 'children'),
    ('sex', 'sexes'),
    ('move', 'moves'),
    #('cow', 'kine') WTF?
]

UNCOUNTABLES = ['equipment', 'information', 'rice', 'money', 'species',
                'series', 'fish', 'sheep']

class Error(Exception):
    """Base exception class for this module."""


class FileObject(object):
    """Represent a 'file' xml entity."""

    def __init__(self, data, name='untitled',
                 content_type='application/octet-stream'):
        self.data = data
        self.name = name
        self.content_type = content_type 


def pluralize(singular):
    """Convert singular word to its plural form.
    
    Args:
        singular: A word in its singular form.
    
    Returns:
        The word in its plural form.
    """
    if singular in UNCOUNTABLES:
        return singular
    for i in IRREGULAR:
        if i[0] == singular:
            return i[1]
    for i in PLURALIZE_PATTERNS:
        if re.search(i[0], singular):
            return re.sub(i[0], i[1], singular)

def singularize(plural):
    """Convert plural word to its singular form.
    
    Args:
        plural: A word in its plural form.
    Returns:
        The word in its singular form.
    """
    if plural in UNCOUNTABLES:
        return plural
    for i in IRREGULAR:
        if i[1] == plural:
            return i[0]
    for i in SINGULARIZE_PATTERNS:
        if re.search(i[0], plural):
            return re.sub(i[0], i[1], plural)
    return plural


def camelize(word):
    """Convert a word from lower_with_underscores to CamelCase.
    
    Args:
        word: The string to convert.
    Returns:
        The modified string.
    """
    return ''.join(w[0].upper() + w[1:]
                   for w in re.sub('[^A-Z^a-z^0-9^:]+', ' ', word).split(' '))


def underscore(word):
    """Convert a word from CamelCase to lower_with_underscores.
    
    Args:
        word: The string to convert.
    Returns:
        The modified string.
    """
    return re.sub(r'\B((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))',
                  r'_\1', word).lower()


def xml_pretty_format(element, level=0):
    """Add PrettyPrint formatting to an ElementTree element.
    
    Args:
        element: An ElementTree element which is modified in-place.
    Returns:
        None
    """
    indent = '\n%s' % ('  ' * level)
    if len(element):
        if not element.text or not element.text.strip():
            element.text = indent + '  '
        for i, child in enumerate(element):
            xml_pretty_format(child, level + 1)
            if not child.tail or not child.tail.strip():
                if i + 1 < len(element):
                    child.tail = indent + "  "
                else:
                    child.tail = indent
    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = indent


def to_xml(obj, root='object', pretty=False, header=True):
    """Convert a dictionary or list to an XML string.
    
    Args:
        obj: The dictionary/list object to convert.
        root: The name of the root xml element.
    Returns:
        An xml string.
    """
    root_element = ET.Element(root.replace('_', '-'))
    if isinstance(obj, list):
        root_element.set('type', 'array')
        for i in obj:
            element = ET.fromstring(
                    to_xml(i, root=singularize(root), header=False))
            root_element.append(element)
    else:
        for key, value in obj.iteritems():
            key = key.replace('_', '-')
            if isinstance(value, dict) or isinstance(value, list):
                element = ET.fromstring(
                    to_xml(value, root=key, header=False))
                root_element.append(element)
            else:
                element = ET.SubElement(root_element, key)
                if value is not None:
                    element.text = str(value)
                    if isinstance(value, int):
                        element.set('type', 'integer')
                else:
                    element.set('nil', 'true')
    if pretty:
        xml_pretty_format(root_element)
    xml_data = ET.tostring(root_element)
    if header:
        return XML_HEADER + '\n' + xml_data
    return xml_data


def xml_to_dict(xmlobj, saveroot=False):
    """Parse the xml into a dictionary of attributes.

    Args:
        xmlobj: An ElementTree element or an xml string.
        saveroot: Keep the xml element names (ugly format)
    Returns:
        A dictionary of attributes (possibly nested).
    """
    if isinstance(xmlobj, basestring):
        # Allow for blank (usually HEAD) result on success
        if xmlobj.isspace():
            return {}
        try:
            element = ET.fromstring(xmlobj)
        except Exception, err:
            raise Error('Unable to parse xml data: %s' % err)
    else:
        element = xmlobj

    element_type = element.get('type', '').lower()
    if element_type == 'array':
        # This is a list, build either a list, or an array like:
        # {list_element_type: [list_element,...]}
        if saveroot:
            child_tag = singularize(element.tag.replace('-', '_'))
            attributes = []
            for child in element.getchildren():
                attribute = xml_to_dict(child, saveroot)
                if isinstance(attribute, dict):
                    attribute = attribute[child_tag]
                attributes.append(attribute)
            return {element.tag.replace('-', '_'): attributes}
        else:
            attributes = [xml_to_dict(e, saveroot)
                          for e in element.getchildren()]
            return attributes

    elif element.get('nil') == 'true':
        return None
    elif element_type in ('integer', 'datetime', 'date', 
                          'decimal', 'double', 'float') and not element.text:
        return None
    elif element_type == 'integer':
        return int(element.text)
    elif element_type == 'datetime':
        if date_parse:
            return date_parse(element.text)
        else:
            timestamp = calendar.timegm(
                    time.strptime(element.text, '%Y-%m-%dT%H:%M:%S+0000'))
            return datetime.datetime.utcfromtimestamp(timestamp)
    elif element_type == 'date':
        time_tuple = time.strptime(element.text, '%Y-%m-%d')
        return datetime.date(*time_tuple[:3])
    elif element_type == 'decimal':
        return decimal.Decimal(element.text)
    elif element_type in ('float', 'double'):
        return float(element.text)
    elif element_type == 'boolean':
        if not element.text:
            return False
        return element.text.strip() in ('true', '1')
    elif element_type == 'yaml':
        if not yaml:
            raise ImportError("PyYaml is not installed: http://pyyaml.org/")
        return yaml.safe_load(element.text)
    elif element_type == 'base64binary':
        return base64.decodestring(element.text)
    elif element_type == 'file':
        content_type = element.get('content_type',
                                   'application/octet-stream')
        filename = element.get('name', 'untitled')
        return FileObject(element.text, filename, content_type)
    elif element_type in ('symbol', 'string'):
        if not element.text:
            return ''
        return element.text
    elif element_type:
        attributes = dict(element.items())
        for child in element.getchildren():
            attributes[child.tag.replace('-', '_')] = child.text
        return attributes
    elif element.getchildren():
        # This is an element with children. The children might be simple
        # values, or nested hashes.
        attributes = {}
        for child in element.getchildren():
            attribute = xml_to_dict(child, saveroot)
            child_tag = child.tag.replace('-', '_')
            if saveroot:
                # If this is a nested hash, it will come back as
                # {child_tag: {key: value}}, we only want the inner hash
                if isinstance(attribute, dict):
                    if len(attribute) == 1 and child_tag in attribute:
                        attribute = attribute[child_tag]
            # Handle multiple elements with the same tag name
            if child_tag in attributes:
                if isinstance(attributes[child_tag], list):
                    attributes[child_tag].append(attribute)
                else:
                    attributes[child_tag] = [attributes[child_tag],
                                             attribute]
            else:
                attributes[child_tag] = attribute
        if saveroot:
            return {element.tag.replace('-', '_'): attributes}
        else:
            return attributes
    else:
        return element.text


def main():
    pass


if __name__ == '__main__':
    main()

