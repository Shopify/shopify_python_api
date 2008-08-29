#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Utilities for pyActiveResource."""

__author__ = 'Mark Roach (mrroach@google.com)'

import re

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

    
def to_xml(o, root='object', pretty=False, header=True):
    """Convert a dictionary or list to an XML string.
    
    Args:
        o: The dictionary/list object to convert.
        root: The name of the root xml element.
    Returns:
        An xml string.
    """
    root_element = ET.Element(root.replace('_', '-'))
    if isinstance(o, list):
        for i in o:
            element = ET.fromstring(
                    to_xml(i, root=singularize(root), header=False))
            root_element.append(element)
    else:
        for key, value in o.iteritems():
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
        try:
            element = ET.fromstring(xmlobj)
        except Exception, e:
            raise Error('Unable to parse xml data.')
    else:
        element = xmlobj

    if element.getchildren():
        is_list = (len(set([e.tag for e in element.getchildren()])) == 1 and 
                       len(element) != 1)

        if element.attrib.get('type') == 'array' or is_list:
            # This is a list, build either a list, or an array like:
            # {list_element_type: [list_element,...]}
            if saveroot:
                attributes = {}
                child_tag = element.getchildren()[0].tag.replace('-', '_')
                attributes[child_tag] = [xml_to_dict(e, saveroot)[child_tag]
                                         for e in element.getchildren()]
            else:
                attributes = [xml_to_dict(e, saveroot)
                              for e in element.getchildren()]
        else:
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
                        attribute = attribute[child_tag]
                attributes[child_tag] = attribute   
        if saveroot:
            return {element.tag.replace('-', '_'): attributes}
        else:
            return attributes
    else:
        # This is a key/value element, convert it to the right type and return
        # only the value.
        if element.get('type') == 'integer':
            if element.text:
                return int(element.text)
            else:
                return None
        elif element.get('nil') == 'true':
            return None
        else:
            return element.text


def main():
    pass


if __name__ == '__main__':
    main()

