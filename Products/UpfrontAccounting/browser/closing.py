from DateTime import DateTime
from Products.Five import BrowserView
from zope.interface import implements, Interface
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money

class IClosingTransfers(Interface):
    """ Marker interface
    """


class ClosingTransfers(BrowserView):

    implements(IClosingTransfers)

    def update(self):
        if self.request.has_key('submit'):
            self.do_transfers()

    def do_transfers(self):
        """ Do closing transfers for given date
        """
        date = self.request.get('closing_transfers_date')
        date = DateTime(date)
        root = self.context.getAccountingRoot()
        root.registerClosingDate(date)
        ledger = root.ledger
        txn_folder = ledger.transactions
        portal_types = getToolByName(self.context, 'portal_types')
        txn_id = ledger.getNextTransactionId()
        txn_folder.invokeFactory(id=txn_id, type_name='Transaction')
        txn = getattr(txn_folder, txn_id)
        txn.edit(
            title='Closing transfers on %s' % date.Date(),
            effectiveDate=date,
            )

        closing_balance = \
            self.context.restrictedTraverse('@@zeromoneyinstance')()
        for account in ledger.accounts.objectValues('Account'):
            if account.getAccountType() not in ('Income', 'Expense'):
                continue
            account.setClosingBalanceForDate(date)
            balance = account.getBalanceForDate(date)
            if balance == 0:
                continue
            closing_balance += balance
            sign = balance > 0 and 'Credit' or 'Debit'
            if balance < 0:
                balance = -balance
            entryId = txn.generateUniqueId('TransactionEntry')
            portal_types.constructContent('TransactionEntry', txn, entryId)
            entry = getattr(txn, entryId)
            entry.edit(
                effectiveDate=date,
                title=account.Title(),
                Description='Closing transfers',
                Account=account,
                DebitCredit=sign,
                Amount=balance,
                )

        retained_income = root.getRetainedIncomeAccount()
        profit_loss = -1 * closing_balance
        sign = profit_loss > 0 and 'Credit' or 'Debit'
        if profit_loss < 0:
            profit_loss = -profit_loss
        entryId = txn.generateUniqueId('TransactionEntry')
        portal_types.constructContent('TransactionEntry', txn, entryId)
        entry = getattr(txn, entryId)
        entry.edit(
            effectiveDate=date,
            title=retained_income.Title(),
            Description='Closing transfers',
            Account=retained_income,
            DebitCredit=sign,
            Amount=profit_loss,
            )

        comment = 'Posted closing transfers for %s' % date.Date()
        txn.portal_workflow.doActionFor( txn, 'post', comment=comment )

        if self.request:
            URL = root.absolute_url()
            self.request.RESPONSE.redirect(
                URL + '?portal_status_message=Closing transfers done')
