# -*- coding: utf-8 -*-
#
# File: testLedger.py
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

from Products.UpfrontAccounting.content.Ledger import Ledger
from Products.FinanceFields.Money import Money
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder


class testLedger(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_getLedger(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        # test acquisition
        accountsfolder = books.ledger.accounts
        self.failUnless(accountsfolder.getLedger() == books.ledger)
        self.failUnless(isinstance(books.ledger, Ledger))

    def test_getNextTransactionId(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
        self.failUnless(isinstance(ledger, Ledger))
        self.failUnless(ledger.getNextTransactionId() != ledger.getNextTransactionId())
        self.failUnless(isinstance(ledger.getNextTransactionId(), basestring))

    def test_getNextAccountId(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
        self.failUnless(isinstance(ledger, Ledger))
        self.failUnless(ledger.getNextAccountId() != ledger.getNextAccountId())
        self.failUnless(isinstance(ledger.getNextAccountId(), basestring))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testLedger))
    return suite

if __name__ == '__main__':
    framework()


