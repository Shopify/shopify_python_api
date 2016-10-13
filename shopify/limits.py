#!/usr/bin/python

############################################################
#
# Copyright 2016 Paladin Logic, Ltd
#           All Rights Reserved
#
############################################################


# Imports
import shopify

CREDIT_LIMIT_HEADER_PARAM = 'x-shopify-shop-api-call-limit'

# Functions
def api_credit_limit_param():
    return shopify.ShopifyResource.connection.response.headers[CREDIT_LIMIT_HEADER_PARAM].split('/')

def credit_left():
    return credit_limit() - credit_used()

available_calls = credit_left

def credit_maxed():
    return credit_left() <= 0

maxed = credit_maxed

def credit_limit():
    return int(api_credit_limit_param()[1])

call_limit = credit_limit

def credit_used():
    return int(api_credit_limit_param()[0])

call_count = credit_used
