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
from zope.interface import providedBy
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.Account import Account
from Products.UpfrontAccounting.content.AccountingFolder import \
    AccountingFolder
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.content.interfaces import IAccount
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.FinanceFields.Money import Money
import StringIO, csv
##/code-section module-beforeclass


class testListTransactionsView(testUpfrontAccounting):
    """Test-cases for class(es) SubsidiaryAccountFolder."""

    ##code-section class-header_testSubsidiaryAccountFolder #fill in your manual code here
    ##/code-section class-header_testSubsidiaryAccountFolder

    def afterSetUp(self):
        #id = 'upfrontbooks'
        #upfrontbooks = portal._getOb(id)
        super(testListTransactionsView, self)._afterSetup()

    # Manually created methods

    def _add_transactionentry(self, transaction, account1, account2, amount):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

        entryid = transaction.generateUniqueId('TransactionEntry')
        portal_types.constructContent('TransactionEntry',
                                      transaction,
                                      entryid,)
        transaction[entryid].edit(Account=account1,
                                  DebitCredit=DEBIT,
                                  Amount=amount)

        te = transaction[entryid]

        entryid = transaction.generateUniqueId('TransactionEntry')
        portal_types.constructContent('TransactionEntry',
                                      transaction,
                                      entryid,)
        transaction[entryid].edit(Account=account2,
                                  DebitCredit=CREDIT,
                                  Amount=amount)

        return (te, transaction[entryid])

    def _add_transaction(self):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
        transactions = getattr(ledger, 'transactions')

        new_transactionid = transactions.generateUniqueId('Transaction')

        portal_types.constructContent('Transaction',
                                      transactions,
                                      new_transactionid,)

        return transactions[new_transactionid]

    def test_batch(self):
        portal = self.getPortal()

        id = 'upfrontbooks'
        books = portal._getOb(id)

        portal_wf = getToolByName(books, 'portal_workflow')

        ledger = getattr(books, 'ledger')
        accounts = getattr(ledger, 'accounts')
        receivables = getattr(books, 'receivables')
        transactions = getattr(ledger, 'transactions')

        self.failUnless(isinstance(accounts, AccountFolder))

        zero = IZeroMoneyInstance(books)()
        for account in accounts.objectValues(spec='Account'):
            if str(account.getBalance()) == str(zero):
                break

        self.failUnless(isinstance(account, Account))

        for account2 in accounts.objectValues(spec='Account'):
            if str(account.getBalance()) == str(zero) and \
                account != account2:
                break

        self.failUnless(isinstance(account2, Account))

        transaction = self._add_transaction()
        transaction = self._add_transaction()

        path = transactions.getPhysicalPath() + ('listtransactions',)

        listtransactions_view = books.restrictedTraverse(path)
        tentries = listtransactions_view.batched_transactions()
        
        self.failUnless(len(tentries) == 2)
        self.failUnless(tentries[0].getObject() != tentries[1].getObject())

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testListTransactionsView))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()





