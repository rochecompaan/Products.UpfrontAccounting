from zope.interface import implements
from zope.component import adapts
from DateTime import DateTime

from Products.FinanceFields.Money import Money
from Products.UpfrontAccounting.interfaces import IAccountTotal, \
    IAccountList
from Products.UpfrontAccounting.content.interfaces import IAccount, \
    IAccountFolder

class AccountTotal(object):

    implements(IAccountTotal)

    adapts(IAccount, IAccountFolder)

    def __init__(self, context):
        self.context = context

    def _getBalancesForDate(self, date):
        """ Compute the total, debit and credit balances for a given
            date
        """
        if date is None: date = DateTime()
        currency = self.context.getAccountingCurrency()
        total = debit = credit = Money('0.00', currency)
        for account in self.context.objectValues():
            if IAccount.providedBy(account):
                balance = account.getBalanceForDate(date)
                total += balance
                if balance > 0:
                    debit += balance
                if balance < 0:
                    credit += -balance
        return total, debit, credit

    def getTotal(self, date=None):
        """ Compute the total for all accounts
        """
        total, debit, credit = self._getBalancesForDate(date)
        return total

    def getDebitTotal(self, date=None):
        """ Total all debit balances
        """
        total, debit, credit = self._getBalancesForDate(date)
        return debit

    def getCreditTotal(self, date=None):
        """ Total all credit balances
        """
        total, debit, credit = self._getBalancesForDate(date)
        return credit

class AccountList(object):
    """ return an account listing with balance as debit or credit for a
        given date.
    """

    implements(IAccountList)

    adapts(IAccount, IAccountFolder)

    def __init__(self, context):
        self.context = context

    def list(self, date, closing_balances=False):
        """ prepare a listing of accounts with debit and credit balances
            for a given date.
        """
        accountlist = []
        accounts = self.context.objectValues()
        # sort on getAccountNumber
        accounts.sort(key=lambda x: x.getAccountNumber())
        for account in accounts:
            if not account.getActive():
                continue

            if closing_balances:
                balance = account.getClosingBalanceForDate(date) 
            else:
                balance = account.getBalanceForDate(date)
            if balance < 0:
                balance = -balance
                isdebit = False
            else:
                isdebit = True

            if balance == 0:
                if account.getAccountType() in ('Asset', 'Expense'):
                    isdebit = True
                else:
                    isdebit = False

            iscredit = not isdebit

            accountlist.append(
                {'obj': account,
                 'path': '/'.join(account.getPhysicalPath()),
                 'relative_url': account.absolute_url(relative=True),
                 'balance': balance,
                 'isdebit': isdebit,
                 'iscredit': iscredit,
                 }
            )

        return accountlist



