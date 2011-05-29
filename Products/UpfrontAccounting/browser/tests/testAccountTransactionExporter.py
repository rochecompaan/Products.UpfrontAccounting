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
from Products.UpfrontAccounting.content.CashBook import CashBook
from Products.UpfrontAccounting.content.AccountingFolder import \
    AccountingFolder
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.FinanceFields.Money import Money
import StringIO, csv
##/code-section module-beforeclass


class testAccountTransactionExporter(testUpfrontAccounting):
    """Test-cases for class(es) SubsidiaryAccountFolder."""

    ##code-section class-header_testSubsidiaryAccountFolder #fill in your manual code here
    ##/code-section class-header_testSubsidiaryAccountFolder

    def afterSetUp(self):
        #id = 'upfrontbooks'
        #upfrontbooks = portal._getOb(id)
        super(testAccountTransactionExporter, self)._afterSetup()

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

        transactions[new_transactionid].setEffectiveDate(DateTime().earliestTime())

        return transactions[new_transactionid]

    def _add_transactionentry(self, transaction, account1, account2, amount):
        portal = self.getPortal()
        portal_types = getToolByName(portal, 'portal_types')

        entryid = transaction.generateUniqueId('TransactionEntry')
        portal_types.constructContent('TransactionEntry',
                                      transaction,
                                      entryid,)
        transaction[entryid].edit(Account=account1,
                                  effectiveDate=DateTime().earliestTime(),
                                  DebitCredit=DEBIT,
                                  Amount=amount)

        entryid = transaction.generateUniqueId('TransactionEntry')
        portal_types.constructContent('TransactionEntry',
                                      transaction,
                                      entryid,)
        transaction[entryid].edit(Account=account2,
                                  effectiveDate=DateTime().earliestTime(),
                                  DebitCredit=CREDIT,
                                  Amount=amount)

    def test_create(self):
        portal = self.getPortal()

        id = 'upfrontbooks'
        books = portal._getOb(id)

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

        transaction = self._add_transaction()
        for i in range(0,2):
            amount = Money(i+2, books.getAccountingCurrency())
            self._add_transactionentry(transaction, account, account2, amount)

        ledger = getattr(books, 'ledger')
        transactions = getattr(ledger, 'transactions')

        portal_wf = getToolByName(portal, 'portal_workflow')
        portal_wf.doActionFor(transaction, 'post')

        path = account.getPhysicalPath() + ('transaction-exporter',)
        exporter = books.restrictedTraverse(path)
        
        exported_csv = exporter()

        self.failUnless(isinstance(exported_csv, basestring))

        f = StringIO.StringIO(exported_csv)
        reader = csv.reader(f, delimiter=',',lineterminator=chr(13))
        rows = []
        for row in reader:
            rows.append(row)

        self.failUnless(len(rows) == 3)
        self.failUnless(rows[0] == ['title', 'TransactionDate', 
                                    'Debit', 'Credit', 'Balance'])

        self.failUnless(rows[1][0] == '')
        self.failUnless(str(rows[1][1]) == str(DateTime().earliestTime()))
        amnt1 = Money(2, books.getAccountingCurrency())
        self.failUnless(rows[1][2] == str(amnt1))
        self.failUnless(rows[1][3] == '')
        amnt2 = Money(5, books.getAccountingCurrency())
        self.failUnless(rows[2][4] == str(amnt2))
                                    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAccountTransactionExporter))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()





