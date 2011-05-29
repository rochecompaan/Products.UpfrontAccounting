# -*- coding: utf-8 -*-
#
# File: testCustomerLedger.py
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

from Products.UpfrontAccounting.content.CustomerLedger import CustomerLedger

from Products.UpfrontAccounting.content.CustomerLedger import \
        CustomerLedger
from Products.FinanceFields.Money import Money
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder


class testCustomerLedger(testUpfrontAccounting):
    """Test-cases for class(es) CustomerLedger."""

    def test_isReceivable(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        receivables =getattr(books, 'receivables')
        self.failUnless(isinstance(receivables, CustomerLedger))

    def test_isPayable(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        receivables =getattr(books, 'receivables')
        self.failUnless(isinstance(receivables, CustomerLedger))

    def test_getNextCreditNoteNumber(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        receivables =getattr(books, 'receivables')
        self.failUnless(isinstance(receivables, CustomerLedger))
        self.failUnless(isinstance(receivables.getNextCreditNoteNumber(), basestring))
        self.failUnless(receivables.getNextCreditNoteNumber() != \
                        receivables.getNextCreditNoteNumber())

    def test_getNextInvoiceNumber(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        receivables =getattr(books, 'receivables')
        self.failUnless(isinstance(receivables, CustomerLedger))
        self.failUnless(isinstance(receivables.getNextInvoiceNumber(), basestring))
        self.failUnless(receivables.getNextInvoiceNumber() != \
                        receivables.getNextInvoiceNumber())

    def test_getNextQuoteNumber(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        receivables =getattr(books, 'receivables')
        self.failUnless(isinstance(receivables, CustomerLedger))
        self.failUnless(isinstance(receivables.getNextQuoteNumber(), basestring))
        self.failUnless(receivables.getNextQuoteNumber() != \
                        receivables.getNextQuoteNumber())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomerLedger))
    return suite

if __name__ == '__main__':
    framework()


