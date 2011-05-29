# -*- coding: utf-8 -*-
#
# File: testCreditNote.py
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

from Products.UpfrontAccounting.content.CreditNote import CreditNote
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.content.AccountFolder import \
        AccountFolder
from Products.UpfrontAccounting.content.CreditNoteFolder import \
        CreditNoteFolder
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.interfaces import ISubsidiaryLedger
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.UpfrontAccounting.content.QuoteFolder import QuoteFolder


class testCreditNote(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_getCustomerAccountTitle(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = portal._getOb(id)

        receivables = getattr(books, 'receivables')
        accounts = getattr(receivables, 'accounts')
        cid = accounts.generateUniqueId('CustomerAccount')
        accounts.invokeFactory(type_name='CustomerAccount', id=cid)
        account = accounts[cid]
        account_title = 'Account Title'
        account.setTitle(account_title)

        creditnotes = getattr(receivables, 'creditnotes')

        self.failUnless(isinstance(creditnotes, CreditNoteFolder))
        cnid = creditnotes.generateUniqueId('CreditNote')
        creditnotes.invokeFactory(type_name='CreditNote', id=cnid)
        cn = getattr(creditnotes, cnid)

        cn.setCustomerAccount(account)

        self.failUnless(cn.getCustomerAccountTitle() == account_title)

    def test_getTaxAmount(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = portal._getOb(id)
        books.setSalesTaxPercentage(10)

        receivables = getattr(books, 'receivables')
        creditnotes = getattr(receivables, 'creditnotes')

        self.failUnless(isinstance(creditnotes, CreditNoteFolder))
        cnid = creditnotes.generateUniqueId('CreditNote')
        creditnotes.invokeFactory(type_name='CreditNote', id=cnid)
        cn = getattr(creditnotes, cnid)

        cn.setCalculateTax(True)
        cn.setAmount(Money(50, books.getAccountingCurrency()))

        self.failUnless(str(cn.getTaxAmount()) ==
                        str(Money(5, books.getAccountingCurrency())))

    def test_getTotal(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = portal._getOb(id)
        books.setSalesTaxPercentage(10)

        receivables = getattr(books, 'receivables')
        creditnotes = getattr(receivables, 'creditnotes')

        self.failUnless(isinstance(creditnotes, CreditNoteFolder))
        cnid = creditnotes.generateUniqueId('CreditNote')
        creditnotes.invokeFactory(type_name='CreditNote', id=cnid)
        cn = getattr(creditnotes, cnid)

        cn.setCalculateTax(True)
        cn.setAmount(Money(50, books.getAccountingCurrency()))

        self.failUnless(str(cn.getTotal()) ==
                        str(Money(55, books.getAccountingCurrency())))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCreditNote))
    return suite

if __name__ == '__main__':
    framework()


