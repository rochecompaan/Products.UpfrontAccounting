# -*- coding: utf-8 -*-
#
# File: testCashbookEntry.py
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

from Products.UpfrontAccounting.content.CashBookEntry import CashBookEntry
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money
from DateTime import DateTime
import string


class testCashbookEntry(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_Title(self):
        entries = self.accountingfolder.cashbook.entries.entriesInOrder()
        self.failUnless(isinstance(entries[0].Title(), basestring))

    def test_setAmount(self):
        entries = self.accountingfolder.cashbook.entries.entriesInOrder()
        self.failUnless(str(entries[0].getAmount()) ==
            str(Money(100,
            self.accountingfolder.cashbook.entries.getAccountingCurrency())))

    def test_isPosted(self):
        entries = self.accountingfolder.cashbook.entries.entriesInOrder()
        self.failUnless(isinstance(entries[0], CashBookEntry))
        self.failUnless(not entries[0].isPosted())

    def test_canPost(self):
        entries = self.accountingfolder.cashbook.entries.entriesInOrder()
        self.failUnless(entries[0].canPost())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCashbookEntry))
    return suite

if __name__ == '__main__':
    framework()


