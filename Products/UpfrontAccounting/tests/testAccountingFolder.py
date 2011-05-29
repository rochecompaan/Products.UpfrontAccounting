# -*- coding: utf-8 -*-
#
# File: testAccountingFolder.py
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

from BTrees.IIBTree import IISet
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.CMFCore.utils import getToolByName
from zope.event import notify
from DateTime import DateTime


class testAccountingFolder(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_instantiation(self):
        # make sure the AccountingFolder is instantiated
        portal = self.getPortal()
        id = 'upfrontbooks'
        upfrontbooks = getattr(portal, id, None)
        self.failUnless(upfrontbooks is not None)
        self.failUnless(isinstance(upfrontbooks, AccountingFolder))

    def test_folderstructure(self):
        # test if the following folders is in AccountingFolder:
        # ledger, receivables, cashbook, payables
        portal = self.getPortal()
        id = 'upfrontbooks'
        upfrontbooks = getattr(portal, id, None)
        self.assertEqual(upfrontbooks['ledger'].getId(), 'ledger')
        self.assertEqual(upfrontbooks['receivables'].getId(), 'receivables')
        self.assertEqual(upfrontbooks['cashbook'].getId(), 'cashbook')
        self.assertEqual(upfrontbooks['payables'].getId(), 'payables')

    def test_accoutingroot(self):
        # make sure the accountingroot is found and returned correctly
        portal = self.getPortal()
        id = 'upfrontbooks'
        upfrontbooks = getattr(portal, id, None)
        self.assertEqual( upfrontbooks.getAccountingRoot(), upfrontbooks)

    def test_closingdates(self):
        # register a closing date and make sure it exists
        portal = self.getPortal()
        id = 'upfrontbooks'
        upfrontbooks = getattr(portal, id, None)
        date = DateTime()
        intdate = int(DateTime(date.Date()))
        upfrontbooks.registerClosingDate(date)
        self.failUnless(
            isinstance(upfrontbooks.getClosingDates(), IISet))
        self.assertEqual([intdate],
                         [d for d in upfrontbooks.getClosingDates()])

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAccountingFolder))
    return suite

if __name__ == '__main__':
    framework()


