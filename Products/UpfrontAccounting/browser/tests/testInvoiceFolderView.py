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

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) 
#

from Testing import ZopeTestCase
from Products.UpfrontAccounting.config import *
from Products.UpfrontAccounting.browser.tests.testUpfrontAccounting import testUpfrontAccounting

# Import the tested classes

##code-section module-beforeclass #fill in your manual code here
from Products.UpfrontAccounting.content.AccountFolder import \
        AccountFolder
from Products.UpfrontAccounting.content.InvoiceFolder import \
        InvoiceFolder
from Products.UpfrontAccounting.content.Invoice import \
        Invoice
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
import StringIO, csv
##/code-section module-beforeclass


class testInvoiceFolderView(testUpfrontAccounting):
    """Test-cases for class(es) SubsidiaryAccountFolder."""

    ##code-section class-header_testSubsidiaryAccountFolder #fill in your manual code here
    ##/code-section class-header_testSubsidiaryAccountFolder

    def afterSetUp(self):
        #id = 'upfrontbooks'
        #upfrontbooks = portal._getOb(id)
        super(testInvoiceFolderView, self)._afterSetup()

    # Manually created methods

    def _add_invoice_item(self, invoice, amount):
        item_id = invoice.generateUniqueId('InvoiceItem')
        item = InvoiceItem(item_id)
        invoice._setObject(item_id, item)
        item = invoice._getOb(item_id)
        item.edit(Rate=amount, Quantity="1.0")

    def _add_invoice(self, folder):
        id = folder.generateUniqueId('Invoice')
        folder.invokeFactory(type_name='Invoice', id=id)
        return folder[id]

    def test_create(self):
        portal = self.getPortal()

        id = 'upfrontbooks'
        books = portal._getOb(id)

        receivables = getattr(books, 'receivables')
        invoices = getattr(receivables, 'invoices')
        self.failUnless(isinstance(invoices, InvoiceFolder))

        today = DateTime().earliestTime()
        yesterday = today - 1
        tomorrow = today + 1
        invoice1 = self._add_invoice(invoices)
        invoice1.edit(InvoiceDate=yesterday)
        invoice2 = self._add_invoice(invoices)
        invoice2.edit(InvoiceDate=today)
        invoice3 = self._add_invoice(invoices)
        invoice3.edit(InvoiceDate=tomorrow)

        path = invoices.getPhysicalPath() + ('folder_contents',)
        folder_view = books.restrictedTraverse(path)
        
        # get the full batch
        batch = folder_view.batched_invoices()
        self.failUnless(len(batch) == 3)

        for b in batch:
            self.failUnless(isinstance(b.getObject(), Invoice))
        
        # check if the start and end dates work
        folder_view.request.set('start_date', today)
        folder_view.request.set('end_date', tomorrow)

        batch = folder_view.batched_invoices()
        self.failUnless(len(batch) == 2)
        self.failUnless(batch[0].getObject() == invoice2)
        self.failUnless(batch[1].getObject() == invoice3)

        # get the center and last entries
        folder_view.request.set('start_date', today)
        folder_view.request.set('end_date', None)

        batch = folder_view.batched_invoices()
        self.failUnless(len(batch) == 2)
        self.failUnless(batch[0].getObject() != batch[1].getObject())
        self.failUnless(batch[0].getObject() in (invoice2, invoice3))
        self.failUnless(batch[1].getObject() in (invoice2, invoice3))

        # get the first and center entries
        folder_view.request.set('start_date', None)
        folder_view.request.set('end_date', today)

        batch = folder_view.batched_invoices()
        self.failUnless(len(batch) == 2)
        self.failUnless(batch[0].getObject() != batch[1].getObject())
        self.failUnless(batch[0].getObject() in (invoice1, invoice2))
        self.failUnless(batch[1].getObject() in (invoice1, invoice2))
 
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testInvoiceFolderView))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()

