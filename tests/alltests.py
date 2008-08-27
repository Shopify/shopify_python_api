#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Test suite for pyactiveresource."""

import unittest

def suite():
    modules_to_test = (
        'activeresource_test',
        )
    alltests = unittest.TestSuite()
    for name in modules_to_test:
        mod = __import__(name)
        for token in name.split('.')[1:]:
            mod = getattr(mod, token)
        alltests.addTest(unittest.findTestCases(mod, suiteClass=None))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')

