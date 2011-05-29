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
from Products.UpfrontAccounting.browser.utils import \
        CashbookEntryAccountVocabularyFactory
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


class testUtils(testUpfrontAccounting):
    """Test-cases for class(es) SubsidiaryAccountFolder."""

    ##code-section class-header_testSubsidiaryAccountFolder #fill in your manual code here
    ##/code-section class-header_testSubsidiaryAccountFolder

    def afterSetUp(self):
        #id = 'upfrontbooks'
        #upfrontbooks = portal._getOb(id)
        super(testUtils, self)._afterSetup()

    # Manually created methods

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

        entryid = transaction.generateUniqueId('TransactionEntry')
        portal_types.constructContent('TransactionEntry',
                                      transaction,
                                      entryid,)

        transaction[entryid].edit(Account=account2,
                                  DebitCredit=CREDIT,
                                  Amount=amount)

    def test_debit_total(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id, None)
        ledger = getattr(books, 'ledger', None)
        accounts = getattr(ledger, 'accounts')

        self.failUnless(isinstance(accounts, AccountFolder))

        zero = IZeroMoneyInstance(books)()
        for account in accounts.objectValues(spec='Account'):
            if str(account.getBalance()) == str(zero):
                break

        self.failUnless(isinstance(account, Account))

        today = DateTime()
        balance = account.getBalanceForDate(today)

        closing = account.getClosingBalanceForDate(today)

        amount = Money(11, books.getAccountingCurrency())
        account.debitAccount(amount, today)
        new_balance = account.getBalanceForDate(today)

        path = list(accounts.getPhysicalPath())
        path.append('debit-total')
        path = tuple(path)
        totalview = account.restrictedTraverse(path)
        
        self.failUnless(str(balance + amount) == str(totalview()))

    def test_credit_total(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id, None)
        ledger = getattr(books, 'ledger', None)
        accounts = getattr(ledger, 'accounts')

        self.failUnless(isinstance(accounts, AccountFolder))

        zero = IZeroMoneyInstance(books)()
        for account in accounts.objectValues(spec='Account'):
            if str(account.getBalance()) == str(zero):
                break

        self.failUnless(isinstance(account, Account))

        today = DateTime()
        balance = account.getBalanceForDate(today)

        closing = account.getClosingBalanceForDate(today)

        amount = Money(11, books.getAccountingCurrency())
        account.creditAccount(amount, today)
        new_balance = account.getBalanceForDate(today)

        path = list(accounts.getPhysicalPath())
        path.append('credit-total')
        path = tuple(path)
        totalview = account.restrictedTraverse(path)
        
        self.failUnless(str(balance + amount) == str(totalview()))

    def test_total(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id, None)
        ledger = getattr(books, 'ledger', None)
        accounts = getattr(ledger, 'accounts')

        self.failUnless(isinstance(accounts, AccountFolder))

        zero = IZeroMoneyInstance(books)()
        for account in accounts.objectValues(spec='Account'):
            if str(account.getBalance()) == str(zero):
                break

        self.failUnless(isinstance(account, Account))

        today = DateTime()
        balance = account.getBalanceForDate(today)

        closing = account.getClosingBalanceForDate(today)

        amount1 = Money(11, books.getAccountingCurrency())
        amount2 = Money(12, books.getAccountingCurrency())
        account.debitAccount(amount1, today)
        account.creditAccount(amount2, today)
        new_balance = account.getBalanceForDate(today)

        accounts.REQUEST.set('filter_date', today)

        path = list(accounts.getPhysicalPath())
        path.append('accounttotal')
        path = tuple(path)
        totalview = account.restrictedTraverse(path)
        
        self.failUnless(str(balance + 
            Money(-1, books.getAccountingCurrency())) == str(totalview()))

    def test_total(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id, None)
        ledger = getattr(books, 'ledger', None)
        accounts = getattr(ledger, 'accounts')

        self.failUnless(isinstance(accounts, AccountFolder))

        zero = IZeroMoneyInstance(books)()
        for account in accounts.objectValues(spec='Account'):
            if str(account.getBalance()) == str(zero):
                break

        self.failUnless(isinstance(account, Account))

        today = DateTime()
        balance = account.getBalanceForDate(today)

        closing = account.getClosingBalanceForDate(today)

        amount1 = Money(11, books.getAccountingCurrency())
        amount2 = Money(12, books.getAccountingCurrency())
        account.debitAccount(amount1, today)
        account.creditAccount(amount2, today)
        new_balance = account.getBalanceForDate(today)

        accounts.REQUEST.set('filter_date', today)

        path = list(accounts.getPhysicalPath())
        path.append('accounttotal')
        path = tuple(path)
        totalview = account.restrictedTraverse(path)
        
        self.failUnless(str(balance + 
            Money(-1, books.getAccountingCurrency())) == str(totalview()))

    def test_listaccounts(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id, None)
        ledger = getattr(books, 'ledger', None)
        accounts = getattr(ledger, 'accounts')

        self.failUnless(isinstance(accounts, AccountFolder))

        path = accounts.getPhysicalPath() + ('listaccounts',)
        listaccountsview = accounts.restrictedTraverse(path)
        accounstlist = listaccountsview(accounttype=None)

        self.failUnless(len(accounstlist) == len(accounts.objectIds()))
    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testUtils))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


