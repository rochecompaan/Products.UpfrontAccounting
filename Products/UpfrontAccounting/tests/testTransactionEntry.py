# -*- coding: utf-8 -*-
#
# File: testTransactionEntry.py
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

from Products.UpfrontAccounting.content.TransactionEntry import \
        TransactionEntry
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


class testTransactionEntry(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_Title(self):
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
        for i in range(0,1):
            amount = Money(i+41, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, CREDIT, amount)

        entries = transaction.entries()
        self.failUnless(isinstance(entries[0].Title(), basestring))

    def test_post(self):
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
        for i in range(0,1):
            amount = Money(i+37, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, CREDIT, amount)

        entries = transaction.entries()
        self.failUnless(len(entries) == 1)
        entries[0].post()

        self.failUnless(entries[0].getAccount() is not None)
        self.failUnless(entries[0] == account.getTransactionEntries()[0])

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

    def test_getTransactionDate(self):
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
        date = DateTime()
        transaction.setEffectiveDate(date)
        for i in range(0,1):
            amount = Money(i+41, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, CREDIT, amount)

        entries = transaction.entries()
        self.failUnless(date == entries[0].getTransactionDate())

    def test_removeTransactionEntryFromAccount(self):
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
            amount = Money(i+37, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, CREDIT, amount)

        entries = transaction.entries()
        for entry in entries:
            entry.post()

        self.failUnless(len(entries) == 3)
        entriesInAccount = account.getTransactionEntries()
        self.failUnless(len(entriesInAccount) == 3)
        self.failUnless(len(entries) == 3)
        entries[1].removeTransactionEntryFromAccount()
        entriesInAccount = account.getTransactionEntries()
        self.failUnless(len(entriesInAccount) == 2)

        for entry in entriesInAccount:
            self.failUnless(entry in entries)

        self.failUnless(str(account.getBalance()) == \
                        str(Money(-76, books.getAccountingCurrency())))

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
    suite.addTest(makeSuite(testTransactionEntry))
    return suite

if __name__ == '__main__':
    framework()


