# -*- coding: utf-8 -*-
#
# File: wfsubscribers.py
#
# Copyright (c) 2010 by Upfront Systems
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Upfront Systems <info@upfrontsystems.co.za>"""
__docformat__ = 'plaintext'


##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.FinanceFields.Money import Money
##/code-section module-header


def postInvoice(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition \
       or event.transition.id not in ['post'] \
       or obj != event.object:
        return
    ##code-section postInvoice #fill in your manual code here

    portal_types = getToolByName(obj, 'portal_types')
    customer_account = obj.getCustomerAccount()
    root = obj.getAccountingRoot()
    customerledger = customer_account.getLedger()
    ledger = root.ledger
    txn_id = str(customerledger.transactions.getNextTransactionId())

    # create transaction inside customer ledger
    customerledger.transactions.invokeFactory(id=txn_id,
        type_name='Transaction')
    transaction = getattr(customerledger.transactions, txn_id)
    transaction.edit(
        title=obj.Title(),
        effectiveDate=obj.getInvoiceDate(),
    )

    def add_entry(account, title, desc, dt_ct, amount):
        if account.id in transaction.objectIds():
            entry = getattr(transaction, account.id)
            amount = entry.getAmount() + amount
            entry.edit(Amount = amount)
        else:
            portal_types.constructContent('TransactionEntry',
                transaction, account.id)
            entry = getattr(transaction, account.id)
            entry.edit(
                Account=account.UID(),
                DebitCredit=dt_ct,
                Amount=amount
                )


    # Credit sales account
    sales_account = obj.getDefaultSalesAccount()
    add_entry(sales_account, 'Sales', 'Sales', 'Credit',
        obj.getConvertedSubTotal())

    # Debit debtor account
    add_entry(customer_account, 'Account', obj.Title(), 'Debit',
        obj.getConvertedSubTotal())

    # Sales Tax
    if obj.getCalculateTax():
        tax_account = customerledger.getSalesTaxAccount()
        tax = obj.getConvertedTaxAmount()
        add_entry(tax_account, 'Tax', 'Tax', 'Credit', tax)
        add_entry(customer_account, 'Tax', 'Tax', 'Debit', tax)

    # Post transaction
    wf_tool = getToolByName(obj, 'portal_workflow')
    wf_tool.doActionFor( transaction, 'post' )


    ##/code-section postInvoice


def postCreditNote(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition \
       or event.transition.id not in ['post'] \
       or obj != event.object:
        return
    ##code-section postCreditNote #fill in your manual code here

    portal_types = getToolByName(obj, 'portal_types')
    creditnote = obj
    customer_account = creditnote.getCustomerAccount()
    root = creditnote.getAccountingRoot()
    customerledger = customer_account.getLedger()
    ledger = root.ledger
    txn_id = str(creditnote.getNextTransactionId())
    customerledger.transactions.invokeFactory(id=txn_id,
        type_name='Transaction')
    transaction = getattr(customerledger.transactions, txn_id)
    transaction.edit(
        title=creditnote.Title(),
        effectiveDate=creditnote.getCreditNoteDate(),
    )

    def add_entry(account, title, desc, dt_ct, amount):
        if account.id in transaction.objectIds():
            entry = getattr(transaction, account.id)
            amount = entry.getAmount() + amount
            entry.edit(Amount = amount)
        else:
            portal_types.constructContent('TransactionEntry',
                transaction, account.id)
            entry = getattr(transaction, account.id)
            entry.edit(
                Account=account.UID(),
                DebitCredit=dt_ct,
                Amount=amount
                )

    # Debit sales account
    sales_account = creditnote.getSalesAccount()
    add_entry(sales_account, 'Sales', 'Sales', 'Debit', creditnote.getAmount())

    # Credit debtor account
    add_entry(customer_account, 'Account', creditnote.Title(), 'Credit',
        creditnote.getAmount())

    # Sales Tax
    tax_account = customerledger.getSalesTaxAccount()
    tax = creditnote.getTaxAmount()
    if tax:
        add_entry(tax_account, 'Tax', 'Tax', 'Debit', tax)
        add_entry(customer_account, 'Tax', 'Tax', 'Credit', tax)

    # Post transaction
    wf_tool = getToolByName(creditnote, 'portal_workflow')
    wf_tool.doActionFor(transaction, 'post' )

    ##/code-section postCreditNote


def undoTransaction(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition \
       or event.transition.id not in ['undo'] \
       or obj != event.object:
        return
    ##code-section undoTransaction #fill in your manual code here
    transaction = obj
    entries = transaction.entries()

    # check if we can undo
    if len(entries) <= 0:
        return

    # force a remove from the balances and update the references
    for transactionEntry in entries:
        transactionEntry.removeTransactionEntryFromAccount()
    ##/code-section undoTransaction


def postCashbookEntryToAccount(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition \
       or event.transition.id not in ['post'] \
       or obj != event.object:
        return
    ##code-section postCashbookEntryToAccount #fill in your manual code here

    zeroMoneyInstance = Money('0.00', obj.getAccountingCurrency())

    cashbookentry = obj
    amount = cashbookentry.getAmount()
    if amount < zeroMoneyInstance:
        amount = -amount

    obj.reindexObject()

    ledger = obj.getAccount().getLedger()
    txn_folder = ledger.transactions
    txn_id = ledger.getNextTransactionId()
    txn_type = 'Transaction'

    portal_types = getToolByName(obj, 'portal_types')

    contra_account = cashbookentry.getAccount()

    if contra_account.portal_type == 'CustomerAccount':
        title = 'Payment received'
    else:
        title = cashbookentry.Description()

    txn_folder.invokeFactory(id=txn_id, type_name=txn_type)
    txn = getattr(txn_folder, txn_id)
    txn.edit(
        title=title,
        effectiveDate=cashbookentry.getDate(),
        )

    # Create entry for cash account
    account = cashbookentry.getBankAccount()
    dt_ct = cashbookentry.getAmount() >= zeroMoneyInstance and DEBIT or CREDIT
    entryid = txn.generateUniqueId('TransactionEntry')
    portal_types.constructContent('TransactionEntry', txn, entryid)
    entry = getattr(txn, entryid)
    entry.edit(
        Account=account,
        DebitCredit=dt_ct,
        Amount=amount
        )

    do_tax = cashbookentry.getTaxIncluded()
    tax_account = obj.getAccountingRoot().ledger.getSalesTaxAccount()
    # Determine if tax should be calculated
    if do_tax:
        tax_rate = obj.getSalesTaxPercentage()
        tax_exclusive_amount = amount - (amount * tax_rate)/(100+tax_rate)

    # Create entry for contra account
    account = cashbookentry.getAccount()
    dt_ct = cashbookentry.getAmount() >= zeroMoneyInstance and CREDIT or DEBIT
    entryid = txn.generateUniqueId('TransactionEntry')
    portal_types.constructContent('TransactionEntry', txn, entryid)
    entry = getattr(txn, entryid)
    entry.edit(
        Account=account,
        DebitCredit=dt_ct,
        Amount=do_tax and tax_exclusive_amount or amount
        )

    # Create entry for tax amount
    if do_tax:
        entryid = txn.generateUniqueId('TransactionEntry')
        portal_types.constructContent('TransactionEntry', txn, entryid)
        entry = getattr(txn, entryid)
        entry.edit(
            Account=tax_account,
            DebitCredit=dt_ct,
            Amount=amount-tax_exclusive_amount
            )

    comment = 'Posted Cashbook entry for %s' % (cashbookentry.Description(),)

    txn.portal_workflow.doActionFor( txn, 'post', comment=comment )
    ##/code-section postCashbookEntryToAccount


def postTransaction(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition \
       or event.transition.id not in ['post'] \
       or obj != event.object:
        return
    ##code-section postTransaction #fill in your manual code here
    for entry in obj.entries():
        entry.post()
    ##/code-section postTransaction



##code-section module-footer #fill in your manual code here
##/code-section module-footer

