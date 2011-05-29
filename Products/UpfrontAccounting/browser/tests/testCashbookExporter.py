# -*- coding: utf-8 -*-
#
# File: testSubsidiaryAccountFolder.py
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

import StringIO, csv
from Testing import ZopeTestCase
from Products.UpfrontAccounting.config import *
from Products.UpfrontAccounting.tests.testUpfrontAccounting import testUpfrontAccounting

from Products.UpfrontAccounting.content.AccountFolder import \
        AccountFolder
from Products.CMFCore.utils import getToolByName
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.Account import Account
from Products.UpfrontAccounting.content.CashBook import CashBook
from Products.UpfrontAccounting.content.AccountingFolder import \
    AccountingFolder
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.FinanceFields.Money import Money


class testCashbookExporter(testUpfrontAccounting):
    """Test-cases for class(es) SubsidiaryAccountFolder."""

    def test_create(self):
        portal = self.getPortal()

        id = 'upfrontbooks'
        books = portal._getOb(id)

        cashbook = getattr(books, 'cashbook')
        self.failUnless(isinstance(cashbook, CashBook))

        for id in cashbook.entries.objectIds():
            cashbook.entries._delObject(id)

        self._add_cashbookentry(3)
        entry = self.cashbook.entries.objectValues()[0]
        entry.edit(title='Rent', ReferenceNumber='I001')

        path = cashbook.getPhysicalPath() + ('cashbook-exporter',)
        exporter = cashbook.restrictedTraverse(path)
        
        exported_csv = exporter()

        self.failUnless(isinstance(exported_csv, basestring))

        f = StringIO.StringIO(exported_csv)
        reader = csv.reader(f, delimiter=',',lineterminator=chr(13))

        rows = []
        for row in reader:
            rows.append(row)

        self.assertEqual(len(rows[0]), 8)
        self.assertEqual(rows[0],
            ['title', 'Date', 'ReferenceNumber', 'Account', 'AccountTitle', 
             'TaxIncluded', 'Amount', 'Balance'])
        row = rows[1]
        self.assertEqual(row[0], entry.Title())
        self.assertEqual(row[1], str(entry.getDate()))
        self.assertEqual(row[2], str(entry.getReferenceNumber()))
        self.assertEqual(row[3], entry.getAccount().getId())
        self.assertEqual(row[4], entry.getAccount().Title())
        self.assertEqual(row[5], str(entry.getTaxIncluded()))
        self.assertEqual(row[6], str(entry.getAmount()))
        self.assertEqual(row[7], str(entry.getAmount()))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCashbookExporter))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()




