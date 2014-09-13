#!/usr/bin/env python

# Copyright (c) 2011 Dan Lecocq
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''Utilities for searching trade-in value'''

import urllib2
import bottlenose
from lxml import objectify


class SearchException(Exception):
    '''An exception for anything that goes wrong in our search'''
    def __init__(self, val):
        Exception.__init__(self, val)
        self.val = val

    def __repr__(self):
        return '%s: %s' % (self.__class__, self.val)

    def __str__(self):
        return repr(self)


class NotEligible(SearchException):
    '''Not eligible for trade in'''
    pass


class NotFound(SearchException):
    '''Not found, 'nuff said'''
    pass


class Search(object):
    '''An object enabling the search of trade-in values'''
    def __init__(self, *args, **kwargs):
        self.amazon = bottlenose.Amazon(*args, **kwargs)

    def __call__(self, sku):
        return self.results(sku)

    def results(self, sku):
        '''Given a SKU, run a search, and print out a representative result.
        Raise an error if it's not eligible, and if it's not found.'''
        try:
            res = self.search(sku)
        except Exception as exp:
            raise SearchException('Error: API error: %s' % exp)

        try:
            item = res.Items.Item
            atts = item.ItemAttributes
        except AttributeError:
            try:
                message = str(res.Items.Request.Errors.Error.Message)
                if 'not a valid value for ItemId' in message:
                    raise NotFound(message)
                else:
                    raise SearchException(message)
            except AttributeError:
                raise SearchException('Unknown error for %s' % sku)

        # Lastly, try to print the thing out
        try:
            item = {
                'title': atts.Title,
                'url':   item.DetailPageURL,
                'price': {
                }
            }
            item['price']['list'] = {
                'amount':   int(atts.ListPrice.Amount),
                'currency': atts.ListPrice.CurrencyCode,
                'format':   atts.ListPrice.FormattedPrice
            }
            item['price']['trade'] = {
                'amount':   int(atts.TradeInValue.Amount),
                'currency': atts.TradeInValue.CurrencyCode,
                'format':   atts.TradeInValue.FormattedPrice
            }
        except AttributeError:
            raise NotEligible(item)
        return item

    def search(self, sku, tipe='EAN'):
        '''Given an items SKU, run a search for the item'''
        for i in range(5):
            try:
                return objectify.fromstring(self.amazon.ItemLookup(
                    ItemId=sku,
                    IdType=tipe,
                    SearchIndex='All',
                    ResponseGroup='ItemAttributes'))
            except urllib2.HTTPError as exc:
                if i == 4:
                    raise exc
                if exc.code == 503:
                    import time
                    print '                Sleeping 1 second...'
                    time.sleep(1)


def pprint(res, level=0):
    '''Pretty-print the lxml objectified object -- useful for debugging'''
    import inspect
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print ('\t' * level) + 'Text: ' + (res.text or '')
    for key, val in inspect.getmembers(res):
        if key[0] in uppercase:
            print ('\t' * level) + key
            pprint(val, level + 1)
