# -*- coding: utf-8 -*-
#
# File: testCustomerAccountFolder.py
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

from Products.UpfrontAccounting.content.CustomerAccountFolder import \
        CustomerAccountFolder
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.content.CustomerAccount import \
        CustomerAccount
from Products.UpfrontAccounting.content.CustomerAccountFolder import \
        CustomerAccountFolder
from Products.UpfrontAccounting.content.CustomerLedger import \
        CustomerLedger
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money
from DateTime import DateTime
import string


class testCustomerAccountFolder(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def afterSetUp(self):
        super(testCustomerAccountFolder, self).afterSetUp()

        portal = self.getPortal()

    def test_getAccountForCustomer(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        CAF = getattr(books, 'receivables')
        self.failUnless(isinstance(CAF, CustomerLedger))

        accountsFolder = getattr(CAF, 'accounts')

        self.failUnless(isinstance(accountsFolder, CustomerAccountFolder))

        # create a few CustomerAccounts, make sure that only one of them is
        # assigned to the customer
        customerAccountId = None
        for i in range(0,3):
            account_id = accountsFolder.generateUniqueId('CustomerAccount')
            accountsFolder.invokeFactory(id=account_id,
                                         type_name='CustomerAccount')
            account = accountsFolder._getOb(account_id)
            title = 'title %s' % i
            account.edit(title=title)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomerAccountFolder))
    return suite

if __name__ == '__main__':
    framework()


