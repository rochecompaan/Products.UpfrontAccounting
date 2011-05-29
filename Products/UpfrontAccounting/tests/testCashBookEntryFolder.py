# -*- coding: utf-8 -*-
#
# File: testCashBook.py
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
from Products.UpfrontAccounting.tests.testUpfrontAccounting import testUpfrontAccounting

# Import the tested classes

##code-section module-beforeclass #fill in your manual code here
from Products.UpfrontAccounting.content.CashBook import CashBook
from Products.FinanceFields.Money import Money
from Products.CMFCore.utils import getToolByName
##/code-section module-beforeclass


class testCashBook(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    ##code-section class-header_testCashBook #fill in your manual code here
    ##/code-section class-header_testCashBook

    def test_getEntriesLastAccount(self):
        # test if the account is computed correctly
        entries = self.cashbook.entries
        accounts = entries.getAccountingRoot().ledger.accounts
        defaultAccountId = accounts.objectIds('Account')[0]
        account = getattr(accounts, defaultAccountId)

        self.assertEqual(entries.getEntriesLastAccount(), account)

    def test_entriesInOrder(self):
        folder = self.cashbook.entries
        entries = folder.entriesInOrder()
        # check that there are the required number of entries
        self.assertEqual(len(entries), 3)

        # check that the entries are in order
        self.assertEqual(
            str(entries[0].getAmount()),
            str(Money(100, folder.getAccountingCurrency()))
            )
        self.assertEqual(
            str(entries[1].getAmount()),
            str(Money(200, folder.getAccountingCurrency())))
        self.assertEqual(
            str(entries[2].getAmount()),
            str(Money(300, folder.getAccountingCurrency()))
            )

    def test_prevBalance(self):
        folder = self.cashbook.entries

        # check previous balance for the third entry
        self.assertEqual(
            str(Money(300, folder.getAccountingCurrency())),
            str(folder.prevBalance('000003'))
            )

        # check previous balance for the second entry
        self.assertEqual(
            str(Money(100, folder.getAccountingCurrency())),
            str(folder.prevBalance('000002'))
            )

    def test_generateUniqueId(self):
        folder = self.cashbook.entries
        entry_id = folder.generateUniqueId('CashbookEntry')
        # check if the id is a string and based on a counter
        self.assertEqual(entry_id, '000004')
        # check that the generated id is incremented
        entry_id = folder.generateUniqueId('CashbookEntry')
        self.assertEqual(entry_id, '000005')

    def test_updateBalance(self):
        folder = self.cashbook.entries
        entries = folder.entriesInOrder()

        folder.updateBalance('000002',
            Money(300, folder.getAccountingCurrency()))

        self.assertEqual(
            str(folder.getBalanceForEntry('000002')),
            str(Money(400, folder.getAccountingCurrency()))
            )
        self.assertEqual(
            str(folder.getBalanceForEntry('000003')),
            str(Money(700, folder.getAccountingCurrency()))
            )

        # now change it back
        folder.updateBalance('000002',
            Money(200, folder.getAccountingCurrency()))

        self.assertEqual(
            str(folder.getBalanceForEntry('000002')),
            str(Money(300, folder.getAccountingCurrency()))
            )
        self.assertEqual(
            str(folder.getBalanceForEntry('000003')),
            str(Money(600, folder.getAccountingCurrency()))
            )


    def test_removeEntryBalance(self):
        folder = self.cashbook.entries
        entries = folder.entriesInOrder()

        folder.removeEntryBalance('000002', keepPosition=False)

        self.assertEqual(
            str(folder.getBalanceForEntry('000001')),
            str(Money(100, folder.getAccountingCurrency()))
            )
        self.assertEqual(
            str(folder.getBalanceForEntry('000003')),
            str(Money(400, folder.getAccountingCurrency()))
            )


    def test_getBalanceForEntry(self):
        folder = self.cashbook.entries

        # test None
        self.assertEqual(
            str(folder.getBalanceForEntry(None)),
            str(Money('0.00', folder.getAccountingCurrency()))
            )

        # check if the balances are correct
        self.assertEqual(
            str(folder.getBalanceForEntry('000001')),
            str(Money(100, folder.getAccountingCurrency()))
            )
        self.assertEqual(
            str(folder.getBalanceForEntry('000002')),
            str(Money(300, folder.getAccountingCurrency()))
            )
        self.assertEqual(
            str(folder.getBalanceForEntry('000003')),
            str(Money(600, folder.getAccountingCurrency()))
            )

        # add an entry
        self._add_cashbookentry(100)

        self.assertEqual(
            str(folder.getBalanceForEntry('000004')),
            str(Money(700, folder.getAccountingCurrency()))
            )

    def test_getPendingEntries(self):
        # test both the review_state and order
        pending_entries = self.cashbook.entries.getPendingEntries()
        self.assertEqual(len(pending_entries), 3)
        for i, entry in enumerate(pending_entries):
            self.assertEqual(entry.getId(), '00000%d' % (i+1))
            self.assertEqual(entry.review_state(), 'pending')

        entry = pending_entries[1]
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.doActionFor(entry, 'post')

        pending_entries = self.cashbook.entries.getPendingEntries()
        self.assertEqual(len(pending_entries), 2)
        self.assertEqual(pending_entries[0].getId(), '000001')
        self.assertEqual(pending_entries[1].getId(), '000003')

        self.cashbook.entries.postTransactions()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCashBook))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


