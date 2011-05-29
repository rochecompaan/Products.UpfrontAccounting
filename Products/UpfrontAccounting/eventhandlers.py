from zope.i18nmessageid import MessageFactory

from Products.UpfrontAccounting.config import PROJECTNAME
from Products.UpfrontAccounting.content.AccountFolder import AccountFolder
from Products.UpfrontAccounting.content.TransactionFolder import \
    TransactionFolder
from Products.UpfrontAccounting.content.CustomerAccountFolder import \
    CustomerAccountFolder
from Products.UpfrontAccounting.content.InvoiceFolder import \
    InvoiceFolder
from Products.UpfrontAccounting.content.InvoiceTemplateFolder import \
    InvoiceTemplateFolder
from Products.UpfrontAccounting.content.QuoteFolder import \
    QuoteFolder
from Products.UpfrontAccounting.content.CreditNoteFolder import \
    CreditNoteFolder
from Products.UpfrontAccounting.content.CashBookEntryFolder import \
    CashBookEntryFolder
from Products.UpfrontAccounting.content.interfaces import ISubsidiaryLedger

_ = MessageFactory(PROJECTNAME)

def cashbookEntryRemoved(ob, event):
    """ A cashbookEntry is removed from the Cashbook
    """
    ob.removeEntryBalance(ob.getId(), keepPosition=False)
    path = '/'.join(ob.getPhysicalPath())
    ob.cashbook_catalog.uncatalog_object(path)

def transactionRemoved(ob, event):
    """ A transaction is removed
    """
    path = '/'.join(ob.getPhysicalPath())
    ob.transaction_catalog.uncatalog_object(path)

def invoiceRemoved(ob, event):
    """ An invoice is removed
    """
    path = '/'.join(ob.getPhysicalPath())
    ob.invoice_catalog.uncatalog_object(path)

def initializeAccountingFolder(ob, event):
    """ Setup the accounting structure for an accounting folder
    """
    # If we are importing an accounting folder it might contain a ledger
    if ob.hasObject('ledger'):
        return

    ob.invokeFactory(type_name='Ledger', id='ledger',
        title=ob.translate('general_ledger_title',
            domain=PROJECTNAME, default='General Ledger')
    )
    ledger = ob.ledger
    accounts = getattr(ledger, 'accounts')

    for category, nr, name, acc_type in ob.account_metadata():
        account_id = ledger.getNextAccountId()
        if name == 'Cheque Account':
            cheque_account_id = account_id
        elif name == 'Accounts Receivable':
            receivables_id = account_id
        elif name == 'Accounts Payable':
            payables_id = account_id
        accounts.invokeFactory(id=account_id, type_name='Account')
        account = getattr(accounts, account_id)
        account.edit(
            title=name,
            AccountNumber=nr,
            AccountType=acc_type)

    # Setup Account Receivables
    control_account = ledger.accounts[receivables_id]
    ob.invokeFactory(type_name='CustomerLedger', id='receivables',
        title=ob.translate('account_receivables_title',
            domain=PROJECTNAME, default='Customers')
    )
    receivables = ob.receivables
    receivables.setInvoicePrefix('AR')
    receivables.setAccountPrefix('A')
    receivables.setTransactionPrefix('AR')
    receivables.setControlAccount(control_account.UID())

    # Setup Account Payables
    control_account = ledger.accounts[payables_id]
    ob.invokeFactory(type_name='SupplierLedger', id='payables',
        title=ob.translate('account_payables_title',
            domain=PROJECTNAME, default='Suppliers')
    )
    payables = ob.payables
    payables.setInvoicePrefix('AP')
    payables.setAccountPrefix('A')
    payables.setTransactionPrefix('AP')
    payables.setControlAccount(control_account.UID())

    # Setup Cashbook
    ob.invokeFactory(type_name='CashBook', id='cashbook',
        title=ob.translate('cashbook_title',
            domain=PROJECTNAME, default='Cashbook')
    )
    cashbook = ob.cashbook
    cheque_account = ledger.accounts[cheque_account_id]
    cashbook.setBankAccount(cheque_account.UID())
    cashbook.manage_permission('Delete objects', roles=[], acquire=0)
    cashbook.manage_permission('Copy or Move', roles=[], acquire=0)
    cashbook.manage_permission('Add portal content', roles=[], acquire=0)

def initializeLedger(ob, event):
    """ Initialize Ledger
    """
    # add transaction catalog
    if not ob.hasObject('transaction_catalog'):
        ob.manage_addProduct['ZCatalog'].manage_addZCatalog(
            'transaction_catalog', 'Transaction Catalog')
        catalog = ob.transaction_catalog
        catalog.addIndex('effective', 'DateIndex', extra=None)
        catalog.addIndex('review_state', 'FieldIndex', extra=None)

    # Don't execute the following steps in the context of a
    # SubsidiaryLedger 
    if ISubsidiaryLedger.providedBy(ob):
        return

    if 'accounts' not in ob.objectIds():
        ob._setObject('accounts', AccountFolder('accounts'))
        ob._getOb('accounts').edit( 
            title=ob.translate(
                'account_folder_title',
                domain=PROJECTNAME,
                default='Accounts', 
            )
        )

    if 'transactions' not in ob.objectIds():
        ob._setObject('transactions', 
            TransactionFolder('transactions'))
        ob._getOb('transactions').edit(
            title=ob.translate(
                'transaction_folder_title',
                domain=PROJECTNAME,
                default='Transactions', 
            )
        )

def initializeCustomerLedger(ob, event):
    """ Setup Customer Ledger
    """
    if 'accounts' not in ob.objectIds():
        ob._setObject('accounts', CustomerAccountFolder('accounts'))
        ob._getOb('accounts').edit(
            title=ob.translate(
                'customeraccount_folder_title',
                domain='UpfrontAccounting',
                default='Accounts'
            )
        )

    if 'transactions' not in ob.objectIds():
        ob._setObject('transactions', 
            TransactionFolder('transactions'))
        ob._getOb('transactions').edit(
            title=ob.translate(
                'transaction_folder_title',
                domain='UpfrontAccounting',
                default='Transactions'
            )
        )

    if 'invoices' not in ob.objectIds():
        ob._setObject('invoices', InvoiceFolder('invoices'))
        ob._getOb('invoices').edit(
            title=ob.translate(
                'invoicefolder_title',
                domain='UpfrontAccounting',
                default='Invoices'
            )
        )
        # add invoices catalog
        if not ob.hasObject('invoice_catalog'):
            ob.manage_addProduct['ZCatalog'].manage_addZCatalog(
                'invoice_catalog', 'Invoice Catalog')
            catalog = ob.invoice_catalog
            catalog.addIndex('getId', 'FieldIndex', extra=None)
            catalog.addIndex('getInvoiceDate', 'DateIndex', extra=None)
            catalog.addIndex('review_state', 'FieldIndex', extra=None)

    if 'invoicetemplates' not in ob.objectIds():
        ob._setObject('invoicetemplates',
            InvoiceTemplateFolder('invoicetemplates'))
        ob._getOb('invoicetemplates').edit(
            title=ob.translate(
                'invoicetemplatefolder_title',
                domain='UpfrontAccounting',
                default='Invoice Templates'
            )
        )

    if 'quotes' not in ob.objectIds():
        ob._setObject('quotes', QuoteFolder('quotes'))
        ob._getOb('quotes').edit(
            title=ob.translate(
                'quotefolder_title',
                domain='UpfrontAccounting',
                default='Quotes'
            )
        )

    if 'creditnotes' not in ob.objectIds():
        ob._setObject('creditnotes', CreditNoteFolder('creditnotes'))
        ob._getOb('creditnotes').edit(
            title=ob.translate(
                'creditnotefolder_title',
                domain='UpfrontAccounting',
                default='Credit Notes'
            )
        )

def initializeCashBook(ob, event):
    """ Initialize CashBook
    """

    # add cashbook catalog
    if not ob.hasObject('cashbook_catalog'):
        ob.manage_addProduct['ZCatalog'].manage_addZCatalog(
            'cashbook_catalog', 'CashBook Catalog')
        catalog = ob.cashbook_catalog
        catalog.addIndex('review_state', 'FieldIndex', extra=None)

    if 'entries' not in ob.objectIds():
        ob._setObject('entries', 
            CashBookEntryFolder('entries'))
        ob._getOb('entries').edit(title=_(u'Entries'))

