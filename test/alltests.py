#!/usr/bin/env python

import unittest

def suite():
    modules_to_test = (
        'article_test',
        'asset_test',
        'base_test',
        'blog_test',
        'cart_test',
        'customer_saved_search_test',
        'fulfillment_test',
        'order_test',
        'product_test',
        'shop_test',
        'transaction_test',
        'variant_test',
        'session_test',
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
