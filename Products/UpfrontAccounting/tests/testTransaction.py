# -*- coding: utf-8 -*-
#
# File: testTransaction.py
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

from Products.UpfrontAccounting.content.Transaction import Transaction
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.content.AccountFolder import \
        AccountFolder
from Products.UpfrontAccounting.content.Account import \
        Account
from Products.UpfrontAccounting.content.TransactionEntry import \
        TransactionEntry
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.interfaces import ISubsidiaryLedger
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.config import DEBIT, CREDIT


class testTransaction(testUpfrontAccounting):
    """Test-cases for class(es) Transaction."""

    def test_entries(self):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

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
        transaction = self._add_transaction()
        for i in range(0,2):
            amount = Money(i+21, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, DEBIT, amount)

        entries = transaction.entries()
        self.failUnless(len(entries) == 2)
        self.failUnless(isinstance(entries[0], TransactionEntry))

    def test_getTotalForSign(self):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

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
        transaction = self._add_transaction()
        for i in range(0,2):
            amount = Money(i+27, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, CREDIT, amount)

        self.failUnless(str(transaction.getCreditTotal()) ==
                        str(Money(55, books.getAccountingCurrency())))
        self.failUnless(str(transaction.getCreditTotal()) ==
                        str(transaction.getTotalForSign(CREDIT)))

    def test_metadata(self):
        pass

    def test_getDebitTotal(self):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

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
        transaction = self._add_transaction()
        for i in range(0,2):
            amount = Money(i+23, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, DEBIT, amount)

        self.failUnless(str(transaction.getDebitTotal()) ==
                        str(Money(47, books.getAccountingCurrency())))

    def test_getTotal(self):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

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
        transaction = self._add_transaction()
        for i in range(0,3):
            amount = Money(i+30, books.getAccountingCurrency())
            sign = i % 2 and DEBIT or CREDIT
            self._add_transactionentry(transaction, account, sign, amount)

        self.failUnless(str(transaction.getTotal()) ==
                        str(Money(-31, books.getAccountingCurrency())))

    def _add_transactionentry(self, transaction, account, debcred, amount):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

        entryid = transaction.generateUniqueId('TransactionEntry')
        portal_types.constructContent('TransactionEntry',
                                      transaction,
                                      entryid,)
        transaction[entryid].edit(Account=account,
                                  DebitCredit=debcred,
                                  Amount=amount)

    def test_getCreditTotal(self):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

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
        transaction = self._add_transaction()
        for i in range(0,2):
            amount = Money(i+25, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, CREDIT, amount)

        self.failUnless(str(transaction.getCreditTotal()) ==
                        str(Money(51, books.getAccountingCurrency())))

    def test_canPostTransaction(self):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

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
        transaction = self._add_transaction()
        for i in range(0,2):
            amount = Money(i+30, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, CREDIT, amount)
            self._add_transactionentry(transaction, account, DEBIT, amount)

        self.failUnless(transaction.canPostTransaction())

    def test_generateUniqueId(self):
        transaction = self._add_transaction()
        self.failUnless(isinstance(transaction, Transaction))
        self.failUnless(isinstance(transaction.generateUniqueId('Transaction'), basestring))
        id1 = transaction.generateUniqueId('Transaction')
        id2 = transaction.generateUniqueId('Transaction')
        self.failUnless(id1 != id2)

    def test_review_state(self):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
        transaction = self._add_transaction()
        self.failUnless(transaction.review_state() == 'pending')

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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testTransaction))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


