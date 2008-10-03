#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Resource format handlers."""

__author__ = 'Mark Roach (mrroach@google.com)'


from pyactiveresource import util


class Base(object):
    """A base format object for inheritance."""
    

class XMLFormat(Base):
    """Read XML formatted ActiveResource objects."""
    
    extension = 'xml'
    mime_type = 'application/xml'
    
    @staticmethod
    def decode(resource_string):
        """Convert a resource string to a dictionary."""
        data = util.xml_to_dict(resource_string, saveroot=True)
        if isinstance(data, dict) and len(data) == 1:
            data = data.values()[0]
        return data

