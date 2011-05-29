# -*- coding: utf-8 -*-
#
# File: testUpfrontAccounting.py
#
# Copyright (c) 2009 by Upfront Systems
# Generator: ArchGenXML 
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Upfront Systems <info@upfrontsystems.co.za>"""
__docformat__ = 'plaintext'

#
# Base TestCase for UpfrontAccounting
#

import os, sys, code
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from DateTime import DateTime
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName

from Products.FinanceFields.Money import Money
from Products.FinanceFields.config import CURRENCY_DISPLAY_LIST
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.config import PRODUCT_DEPENDENCIES
from Products.UpfrontAccounting.config import DEPENDENCIES

# Add common dependencies
PRODUCT_DEPENDENCIES.append('MimetypesRegistry')
PRODUCT_DEPENDENCIES.append('PortalTransforms')
PRODUCT_DEPENDENCIES.append('UpfrontAccounting')

# Install all (product-) dependencies, install them too
for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
    ZopeTestCase.installProduct(dependency)

ZopeTestCase.installProduct('UpfrontAccounting')

PRODUCTS = list()
PRODUCTS += DEPENDENCIES
PRODUCTS.append('UpfrontAccounting')

testcase = PloneTestCase.PloneTestCase
ZopeTestCase.installProduct('ZCatalog', 1)

PloneTestCase.setupPloneSite(products=PRODUCTS)

class testUpfrontAccounting(testcase):
    """Base TestCase for UpfrontAccounting."""


    def _setupUser(self):
        '''Creates the default user.'''
        self.portal.manage_permission(
            'Add portal member', roles=[], acquire=1)
        uf = self.portal.acl_users
        uf.userFolderAddUser(ZopeTestCase.user_name,
            ZopeTestCase.user_password, ['Member'], [])

    def afterSetUp(self):
        """
        """
        self.setRoles(('Manager',))
        portal = self.getPortal()
        portal.error_log._ignored_exceptions = ()

        portal_url = portal.absolute_url()

        id = 'upfrontbooks'

        upfrontbooks = AccountingFolder(id, id=id,
            AccountingCurrency=CURRENCY_DISPLAY_LIST[0])

        upfrontbooks.setAccountingCurrency(CURRENCY_DISPLAY_LIST[0])

        rval = portal._setObject(id, upfrontbooks)
        newid = isinstance(rval, basestring) and rval or id

        upfrontbooks = portal._getOb(newid)
        taxaccount = self.portal.portal_catalog(
            Title='Sales Tax Control Account',
            portal_type='Account')[0].getObject()
        upfrontbooks.setSalesTaxAccount(taxaccount)
        upfrontbooks.setSalesTaxPercentage(10)
        self.accountingfolder = upfrontbooks

        # add a few cashbookentries to the cashbook, making sure the
        # values are unique and nonzero
        self.cashbook = self.accountingfolder.cashbook
        for i in range(1, 4):
            self._add_cashbookentry(i*100)


    def _add_cashbookentry(self, amount, account=None):
        cashbook = self.cashbook

        # Add a new item
        if account is None:
            account = self.accountingfolder.ledger.accounts.objectValues()[0]

        itemid = cashbook.entries.generateUniqueId(type_name='CashBookEntry')
        portal_types = getToolByName(self.cashbook, 'portal_types')
        entries = self.cashbook.entries
        portal_types.constructContent('CashBookEntry', entries, itemid)

        entry = entries[itemid]
        entry.edit(
            Date=DateTime(0)+int(itemid),
            Amount=Money(amount, cashbook.getAccountingCurrency()),
            AccountType='Ledger',
            Account=account)

        return entry


    def interact(self, locals=None):
        """Provides an interactive shell aka console inside your testcase.

        It looks exact like in a doctestcase and you can copy and paste
        code from the shell into your doctest. The locals in the testcase are
        available, becasue you are in the testcase.

        In your testcase or doctest you can invoke the shell at any point by
        calling::

            >>> self.interact( locals() )

        locals -- passed to InteractiveInterpreter.__init__()
        """
        savestdout = sys.stdout
        sys.stdout = sys.stderr
        sys.stderr.write('='*70)
        console = code.InteractiveConsole(locals)
        console.interact("""
ZopeTestCase Interactive Console
(c) BlueDynamics Alliance, Austria - 2005

Note: You have the same locals available as in your test-case.
""")
        sys.stdout.write('\nend of ZopeTestCase Interactive Console session\n')
        sys.stdout.write('='*70+'\n')
        sys.stdout = savestdout


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testUpfrontAccounting))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


