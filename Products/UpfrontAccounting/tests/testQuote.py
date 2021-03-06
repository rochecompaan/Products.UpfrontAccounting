# -*- coding: utf-8 -*-
#
# File: testQuote.py
#
# Copyright (c) 2009 by Upfront Systems
# Generator: ArchGenXML 
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Upfront Systems <info@upfrontsystems.co.za>"""
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.UpfrontAccounting.config import *
from Products.UpfrontAccounting.tests.testUpfrontAccounting import testUpfrontAccounting

from Products.UpfrontAccounting.content.Quote import Quote
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.content.AccountFolder import \
        AccountFolder
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.interfaces import ISubsidiaryLedger
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.UpfrontAccounting.content.QuoteFolder import QuoteFolder


class testQuote(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_instantiation(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = portal._getOb(id)
        receivables = getattr(books, 'receivables')
        quotes = getattr(receivables, 'quotes')

        self.failUnless(isinstance(quotes, QuoteFolder))

        qid = quotes.generateUniqueId('Quote')
        quotes.invokeFactory(type_name='Quote', id=qid)

        self.failUnless(isinstance(getattr(quotes, qid), Quote))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testQuote))
    return suite

if __name__ == '__main__':
    framework()


