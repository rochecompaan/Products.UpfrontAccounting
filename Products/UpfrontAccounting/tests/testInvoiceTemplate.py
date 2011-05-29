# -*- coding: utf-8 -*-
#
# File: testInvoiceTemplate.py
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

from Products.UpfrontAccounting.content.InvoiceTemplate import \
        InvoiceTemplate
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.content.AccountFolder import \
        AccountFolder
from Products.UpfrontAccounting.content.InvoiceTemplateFolder import \
        InvoiceTemplateFolder
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.interfaces import ISubsidiaryLedger
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.UpfrontAccounting.content.QuoteFolder import QuoteFolder


class testInvoiceTemplate(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def afterSetUp(self):
        super(testInvoiceTemplate, self).afterSetUp()

    def test_instantiation(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        receivables = getattr(books, 'receivables')
        invoicetemplates = getattr(receivables, 'invoicetemplates')

        self.failUnless(isinstance(invoicetemplates, InvoiceTemplateFolder))
        itid=invoicetemplates.generateUniqueId('InvoiceTemplate')
        invoicetemplates.invokeFactory(type_name='InvoiceTemplate', id=itid)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testInvoiceTemplate))
    return suite

if __name__ == '__main__':
    framework()


