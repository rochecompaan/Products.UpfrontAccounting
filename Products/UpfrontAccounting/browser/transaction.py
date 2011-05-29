from Products.Five import BrowserView
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.exceptions import AccessControl_Unauthorized

class Transaction(BrowserView):
    def reverse_transaction(self):
        """ Reverse a transaction - create a debit for a credit and a credit
            for a debit for each transaction entry
        """
        portal_types = getToolByName(self.context, 'portal_types')

        transaction = self.context
        entries = transaction.entries()

        # check if there are transaction entries
        if not transaction.canUndoOrReverse():
            raise AccessControl_Unauthorized('No permission to create transactionentries, or there are no entries to reverse')

        # add the new reversal transaction
        transaction_folder = transaction.getTransactionFolder()
        new_transactionid = transaction_folder.generateUniqueId('Transaction')

        portal_types.constructContent('Transaction',
                                        transaction_folder,
                                        new_transactionid,)

        new_transaction = transaction_folder[new_transactionid]
        # create all the reverse transactions
        for transactionEntry in entries:
            entryid = new_transaction.generateUniqueId('TransactionEntry')
            portal_types.constructContent('TransactionEntry',
                                            new_transaction,
                                            entryid,)
            debit_credit = DEBIT
            if transactionEntry.getDebitCredit() == DEBIT:
                debit_credit = CREDIT
            new_transaction[entryid].edit(Account=transactionEntry.getAccount(),
                                        DebitCredit=debit_credit,
                                        Amount=transactionEntry.getAmount())

        self.request.response.redirect(new_transaction.absolute_url()+ '/view')
 
    def undo_transaction(self):
        """ Undo a transaction - remove the reference to the transaction, and
            do a debit/credit as necessary
        """
        transaction = self.context
        entries = transaction.entries()

        # check if we can undo
        if not transaction.canUndoOrReverse():
            raise AccessControl_Unauthorized('No permission to create transactionentries, or there are no entries to reverse')
        
        # force a remove from the balances and update the references
        for transactionEntry in entries:
            transactionEntry.removeTransactionEntryFromAccount()

        # remove transaction
        transaction.getTransactionFolder().manage_delObjects(ids=transaction.getId())

class TransactionView(BrowserView):
    """
    """
    def transactionEntries(self):
        """
        """
        return self.context.objectValues()

