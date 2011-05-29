# -*- coding: utf-8 -*-
#
# File: testAccount.py
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

from Products.UpfrontAccounting.content.Account import Account
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.content.AccountFolder import \
        AccountFolder
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.interfaces import ISubsidiaryLedger
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.config import DEBIT, CREDIT


class testAccount(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_setClosingBalanceForDate(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
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
        self.failUnless(str(balance) == str(closing) and
                        str(balance) == str(zero))
        amount = Money(7, books.getAccountingCurrency())
        account.creditAccount(amount, today)
        account.setClosingBalanceForDate(today)

        self.failUnless(str(account.getClosingBalanceForDate(today)) ==
                        str(-amount))

        # cannot set two closing balances
        self.assertRaises(RuntimeError, 
                          account.setClosingBalanceForDate,
                          today)

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

    def test_getClosingBalanceForDate(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
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
        self.failUnless(str(balance) == str(closing) and
                        str(balance) == str(zero))
        amount = Money(8, books.getAccountingCurrency())
        account.debitAccount(amount, today)
        account.setClosingBalanceForDate(today)

        self.failUnless(str(account.getClosingBalanceForDate(today)) ==
                        str(amount))

    def test_getBalanceForDate(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
        accounts = getattr(ledger, 'accounts')
        self.failUnless(isinstance(accounts, AccountFolder))

        account = accounts.objectValues(spec='Account')[0]
        self.failUnless(isinstance(account, Account))

        today = DateTime()
        balance = account.getBalanceForDate(today)
        self.failUnless(isinstance(balance, Money))

    def test_debitAccount(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
        accounts = getattr(ledger, 'accounts')
        self.failUnless(isinstance(accounts, AccountFolder))

        zero = IZeroMoneyInstance(books)()
        for account in accounts.objectValues(spec='Account'):
            if str(account.getBalance()) == str(zero):
                break

        self.failUnless(isinstance(account, Account))

        today = DateTime()
        balance = account.getBalanceForDate(today)

        amount = Money(11, books.getAccountingCurrency())
        account.debitAccount(amount, today)
        new_balance = account.getBalanceForDate(today)

        self.failUnless(str(balance + amount) == str(new_balance))

    def test_transactionEntriesAndBalances(self):
        portal = self.getPortal()
        portal_wf = getToolByName(portal, 'portal_workflow')

        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
        accounts = getattr(ledger, 'accounts')
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

        today = DateTime()

        # there is quite a bit of setup necessary to get a transaction
        # into the TransactionEntries field.  First, a transaction entry
        # must be inserted in a transaction folder, an opposite
        # transactionentry must be inserted, and then the transaction must
        # be posted. Only then can we test if the method works

        transaction = self._add_transaction()
        for i in range(0,2):
            amount = Money(i+17, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, account2, amount)

        portal_wf.doActionFor(transaction, 'post')

        entriesNbalances = account.getTransactionEntriesAndBalances()

        self.failUnless(len(entriesNbalances) == 2)
        self.failUnless(str(entriesNbalances[0].balance) == \
                        str(Money(17, books.getAccountingCurrency())))
        self.failUnless(str(entriesNbalances[1].balance) == \
                        str(Money(35, books.getAccountingCurrency())))

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

    def test_creditAccount(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
        accounts = getattr(ledger, 'accounts')
        self.failUnless(isinstance(accounts, AccountFolder))

        zero = IZeroMoneyInstance(books)()
        for account in accounts.objectValues(spec='Account'):
            if str(account.getBalance()) == str(zero):
                break

        self.failUnless(isinstance(account, Account))

        today = DateTime()
        balance = account.getBalanceForDate(today)

        amount = Money(12, books.getAccountingCurrency())
        account.creditAccount(amount, today)
        new_balance = account.getBalanceForDate(today)

        self.failUnless(str(balance - amount) == str(new_balance))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAccount))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


