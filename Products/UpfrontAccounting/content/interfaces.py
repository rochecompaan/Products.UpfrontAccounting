# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class IAccount(Interface):
    """Marker interface for .Account.Account
    """

class IAccountFolder(Interface):
    """Marker interface for .AccountFolder.AccountFolder
    """

class IAccountingFolder(Interface):
    """Marker interface for .AccountingFolder.AccountingFolder
    """

class ILedger(Interface):
    """Marker interface for .Ledger.Ledger
    """

class ICashBook(Interface):
    """Marker interface for .CashBook.CashBook
    """

class ISubsidiaryLedger(Interface):
    """Marker interface for .SubsidiaryLedger.SubsidiaryLedger
    """

class ICustomerLedger(Interface):
    """Marker interface for .CustomerLedger.CustomerLedger
    """

class ISupplierLedger(Interface):
    """Marker interface for .SupplierLedger.SupplierLedger
    """

class ITransactionFolder(Interface):
    """Marker interface for .TransactionFolder.TransactionFolder
    """

class ITransaction(Interface):
    """Marker interface for .Transaction.Transaction
    """

class ITransactionEntry(Interface):
    """Marker interface for .TransactionEntry.TransactionEntry
    """

class ICashBookEntry(Interface):
    """Marker interface for .CashBookEntry.CashBookEntry
    """

class ICustomerAccountFolder(Interface):
    """Marker interface for .CustomerAccountFolder.CustomerAccountFolder
    """

class ICustomerAccount(Interface):
    """Marker interface for .CustomerAccount.CustomerAccount
    """

class IInvoiceFolder(Interface):
    """Marker interface for .InvoiceFolder.InvoiceFolder
    """

class IInvoice(Interface):
    """Marker interface for .Invoice.Invoice
    """

class IInvoiceItem(Interface):
    """Marker interface for .InvoiceItem.InvoiceItem
    """

class IQuoteFolder(Interface):
    """Marker interface for .QuoteFolder.QuoteFolder
    """

class IQuote(Interface):
    """Marker interface for .Quote.Quote
    """

class ICreditNoteFolder(Interface):
    """Marker interface for .CreditNoteFolder.CreditNoteFolder
    """

class ICreditNote(Interface):
    """Marker interface for .CreditNote.CreditNote
    """

class ISubsidiaryAccount(Interface):
    """Marker interface for .SubsidiaryAccount.SubsidiaryAccount
    """

class ISubsidiaryAccountFolder(Interface):
    """Marker interface for .SubsidiaryAccountFolder.SubsidiaryAccountFolder
    """

class IInvoiceTemplateFolder(Interface):
    """Marker interface for .InvoiceTemplateFolder.InvoiceTemplateFolder
    """

class IInvoiceTemplate(Interface):
    """Marker interface for .InvoiceTemplate.InvoiceTemplate
    """

class IOrderedBTreeContainer(Interface):
    """Marker interface for .OrderedBTreeContainer.OrderedBTreeContainer
    """

class ICashBookEntryFolder(Interface):
    """Marker interface for .CashBookEntryFolder.CashBookEntryFolder
    """

##code-section FOOT
##/code-section FOOT