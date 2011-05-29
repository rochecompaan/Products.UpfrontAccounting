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
from Products.CMFCore.utils import getToolByName
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.Account import Account
from Products.UpfrontAccounting.content.AccountingFolder import \
    AccountingFolder
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.FinanceFields.Money import Money
##/code-section module-beforeclass


class testAdding(testUpfrontAccounting):
    """Test-cases for class(es) SubsidiaryAccountFolder."""

    ##code-section class-header_testSubsidiaryAccountFolder #fill in your manual code here
    ##/code-section class-header_testSubsidiaryAccountFolder

    def afterSetUp(self):
        #id = 'upfrontbooks'
        #upfrontbooks = portal._getOb(id)
        super(testAdding, self)._afterSetup()

    # Manually created methods

    def test_create(self):
        portal = self.getPortal()

        path = portal.getPhysicalPath() + ('addAccountingFolder',)
        
        addview = portal.restrictedTraverse(path)
        
        folder = addview.create({'title':'testAccFol', 'currency':'ZAR'})
        self.failUnless(isinstance(folder, AccountingFolder))
        self.failUnless(folder.Title() == 'testAccFol')
        self.failUnless(folder.getAccountingCurrency() == 'ZAR')

    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAdding))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()



