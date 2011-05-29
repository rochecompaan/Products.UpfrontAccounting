# -*- coding: utf-8 -*-
#
# File: testInvoice.py
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

from Products.UpfrontAccounting.content.Invoice import Invoice
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.content.AccountFolder import \
        AccountFolder
from Products.UpfrontAccounting.content.InvoiceFolder import \
        InvoiceFolder
from Products.UpfrontAccounting.content.InvoiceItem import \
        InvoiceItem
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.interfaces import ISubsidiaryLedger
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.config import DEBIT, CREDIT


class testInvoice(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_getSubTotal(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        receivables = getattr(books, 'receivables')
        invoices = getattr(receivables, 'invoices')

        self.failUnless(isinstance(invoices, InvoiceFolder))
        invoice = self._add_invoice(invoices)

        self.failUnless(isinstance(invoice, Invoice))

        self.failUnless(str(invoice.getSubTotal()) ==
                        str(Money(0, books.getAccountingCurrency())))

        self._add_invoice_item(invoice, Money(53, books.getAccountingCurrency()))
        self._add_invoice_item(invoice, Money(54, books.getAccountingCurrency()))

        self.failUnless(str(invoice.getSubTotal()) ==
                        str(Money(107, books.getAccountingCurrency())))

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

    def test_getTotal(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)
        books.setSalesTaxPercentage(10)

        receivables = getattr(books, 'receivables')
        invoices = getattr(receivables, 'invoices')

        self.failUnless(isinstance(invoices, InvoiceFolder))
        invoice = self._add_invoice(invoices)

        self.failUnless(isinstance(invoice, Invoice))

        invoice.setCalculateTax(False)

        self.failUnless(str(invoice.getTotal()) ==
                        str(Money(0, books.getAccountingCurrency())))

        self._add_invoice_item(invoice, Money(53, books.getAccountingCurrency()))
        self._add_invoice_item(invoice, Money(54, books.getAccountingCurrency()))

        self.failUnless(str(invoice.getTotal()) == str(invoice.getSubTotal()))

        invoice.setCalculateTax(True)

        self.failUnless(str(invoice.getTotal()) ==
                        str(Money("117.7", books.getAccountingCurrency())))

    def test_generateUniqueId(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        receivables = getattr(books, 'receivables')
        invoices = getattr(receivables, 'invoices')

        self.failUnless(isinstance(invoices, InvoiceFolder))
        self.failUnless(isinstance(invoices.generateUniqueId('InvoiceItem'),
                        basestring))
        self.failUnless(invoices.generateUniqueId('InvoiceItem') !=
                        invoices.generateUniqueId('InvoiceItem'))

    def test_getTaxAmount(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)
        books.setSalesTaxPercentage(10)

        receivables = getattr(books, 'receivables')
        invoices = getattr(receivables, 'invoices')

        self.failUnless(isinstance(invoices, InvoiceFolder))
        invoice = self._add_invoice(invoices)

        self.failUnless(isinstance(invoice, Invoice))

        self.failUnless(str(invoice.getTotal()) ==
                        str(Money(0, books.getAccountingCurrency())))

        self._add_invoice_item(invoice, Money(53, books.getAccountingCurrency()))
        self._add_invoice_item(invoice, Money(54, books.getAccountingCurrency()))

        invoice.setCalculateTax(True)

        self.failUnless(str(invoice.getTaxAmount()) ==
                        str(Money("10.70", books.getAccountingCurrency())))

    def test_review_state(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)
        books.setSalesTaxPercentage(10)

        receivables = getattr(books, 'receivables')
        invoices = getattr(receivables, 'invoices')

        self.failUnless(isinstance(invoices, InvoiceFolder))
        invoice = self._add_invoice(invoices)

        self.failUnless(isinstance(invoice, Invoice))
        self.failUnless(invoice.review_state() == 'pending')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testInvoice))
    return suite

if __name__ == '__main__':
    framework()


