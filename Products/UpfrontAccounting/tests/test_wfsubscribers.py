# -*- coding: utf-8 -*-
#
# File: test_wfsubscribers.py
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
from Products.FinanceFields.Money import Money
from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from Products.UpfrontAccounting.config import *
from Products.UpfrontAccounting.tests.testUpfrontAccounting import testUpfrontAccounting
from Products.UpfrontAccounting import wfsubscribers

class test_wfsubscribers(testUpfrontAccounting):
    """ Test-cases for class(es). """

    def test_postInvoice(self):
        # set tax rate to 10%
        self.accountingfolder.setSalesTaxPercentage(10)
        salesaccount = self.portal.portal_catalog(
            Title='Sales', portal_type='Account')[0].getObject()
        self.accountingfolder.setDefaultSalesAccount(salesaccount)

        # create a customer account
        receivables = self.accountingfolder.receivables
        accounts = receivables.accounts
        accounts.invokeFactory(type_name='CustomerAccount', id='customer')
        customeraccount = accounts._getOb('customer')

        # add an invoice
        invoices = receivables.invoices
        invoice_id = invoices.generateUniqueId(type_name='Invoice')
        invoices.invokeFactory(type_name='Invoice', id=invoice_id,
            CustomerAccount=customeraccount, InvoiceCurrency='AED')
        invoice = invoices._getOb(invoice_id)

        # add a invoice item
        item_id = invoice.generateUniqueId(type_name='InvoiceItem')
        invoice.invokeFactory(type_name="InvoiceItem", id=item_id)
        item = invoice._getOb(item_id)
        item.edit(description='Consulting', Quantity=1, Unit='hour',
            Rate='AED 100.00')

        wftool = getToolByName(invoice, 'portal_workflow')
        wftool.doActionFor(invoice, 'post')

        last_txn = receivables.transactions.objectValues()[-1]

        first_txn_entry = last_txn.objectValues()[0]
        second_txn_entry = last_txn.objectValues()[1]
        third_txn_entry = last_txn.objectValues()[2]

        taxaccount = self.accountingfolder.ledger.getSalesTaxAccount()

        self.assertEqual(
            first_txn_entry.getAccount().UID(), salesaccount.UID())
        self.assertEqual(
            first_txn_entry.getAmount(),
            invoice.getSubTotal()
            )
        self.assertEqual(
            first_txn_entry.getDebitCredit(), CREDIT)

        self.assertEqual(
            second_txn_entry.getAccount().UID(), customeraccount.UID())
        self.assertEqual(
            second_txn_entry.getAmount(),
            invoice.getTotal())
        self.assertEqual(
            second_txn_entry.getDebitCredit(), DEBIT)

        self.assertEqual(
            third_txn_entry.getAccount().UID(), taxaccount.UID())
        self.assertEqual(
            third_txn_entry.getAmount(),
            invoice.getTaxAmount()
            )
        self.assertEqual(
            third_txn_entry.getDebitCredit(), CREDIT)


    def test_postCashbookEntryToAccount(self):
        # add and entry for an expense with sales tax
        account = self.portal.portal_catalog(Title='Bank Charges',
            portal_type='Account')[0].getObject()
        cashbookaccount = self.cashbook.getBankAccount()
        taxaccount = self.accountingfolder.ledger.getSalesTaxAccount()

        entry = self._add_cashbookentry(-110, account)
        entry.edit(TaxIncluded=True)
        wftool = getToolByName(entry, 'portal_workflow')
        wftool.doActionFor(entry, 'post')

        last_txn = self.accountingfolder.ledger.transactions.objectValues()[-1]
        self.assertEqual(last_txn.getEffectiveDate(), entry.getDate())

        first_txn_entry = last_txn.objectValues()[0]
        second_txn_entry = last_txn.objectValues()[1]
        third_txn_entry = last_txn.objectValues()[2]
        amount = entry.getAmount()

        # a transaction entry amount is always positive
        if amount < 0:
            amount = -amount

        self.assertEqual(
            first_txn_entry.getAccount().UID(), cashbookaccount.UID())
        self.assertEqual(
            first_txn_entry.getAmount(), amount)
        self.assertEqual(
            first_txn_entry.getDebitCredit(), CREDIT)

        self.assertEqual(
            second_txn_entry.getAccount().UID(), entry.getAccount().UID())
        self.assertEqual(
            second_txn_entry.getAmount(),
            Money(100, self.cashbook.getAccountingCurrency())
            )
        self.assertEqual(
            second_txn_entry.getDebitCredit(), DEBIT)

        self.assertEqual(
            third_txn_entry.getAccount().UID(), taxaccount.UID())
        self.assertEqual(
            third_txn_entry.getAmount(),
            Money(10, self.cashbook.getAccountingCurrency())
            )
        self.assertEqual(
            third_txn_entry.getDebitCredit(), DEBIT)

        # test a payment by a customer 

        # add a customer account
        accounts = self.accountingfolder.receivables.accounts
        account_id = accounts.getNextAccountId()
        accounts.invokeFactory(id=account_id, type_name='CustomerAccount')
        customeraccount = getattr(accounts, account_id)
        customeraccount.edit(title='Customer Account')

        entry = self._add_cashbookentry(110, customeraccount)
        wftool = getToolByName(entry, 'portal_workflow')
        wftool.doActionFor(entry, 'post')

        last_txn = \
            self.accountingfolder.receivables.transactions.objectValues()[-1]
        self.assertEqual(last_txn.getEffectiveDate(), entry.getDate())

        first_txn_entry = last_txn.objectValues()[0]
        second_txn_entry = last_txn.objectValues()[1]
        amount = entry.getAmount()

        # a transaction entry amount is always positive
        if amount < 0:
            amount = -amount

        self.assertEqual(
            first_txn_entry.getAccount().UID(), cashbookaccount.UID())
        self.assertEqual(
            first_txn_entry.getAmount(), amount)
        self.assertEqual(
            first_txn_entry.getDebitCredit(), DEBIT)

        self.assertEqual(
            second_txn_entry.getAccount().UID(), entry.getAccount().UID())
        self.assertEqual(second_txn_entry.getAmount(), amount)
        self.assertEqual(second_txn_entry.getDebitCredit(), CREDIT)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(test_wfsubscribers))
    return suite

if __name__ == '__main__':
    framework()



