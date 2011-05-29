import csv
from cStringIO import StringIO

from zope.interface import implements
from zope.component import adapts

from Products.UpfrontAccounting.interfaces \
    import ICSVWriter, IAccountList
from Products.UpfrontAccounting.content.interfaces import IAccount, \
    IAccountFolder
from DateTime import DateTime

class AccountCSVWriter(object):

    implements(ICSVWriter)

    adapts(IAccount, IAccountFolder)

    def __init__(self, context):
        self.context = context
        self.request = context.request

    def _get_date(self):
        """ Get the date from the request
        """
        date = self.request.get('filter_date', DateTime().Date())
        date = DateTime(date)
        return date

    def write(self):
        """ Return account balances for a given date as CSV file. We
            return a StringIO instance to allow streaming of the output if
            required.
        """
        output = StringIO()
        writer = csv.writer(output)
        date = self._get_date()
        if not date:
            return output

        heading = 'Account balances for %s' % date.Date()
        writer.writerow([heading, '', '', '', '', ''])
        columns = ('id', 'title', 'AccountNumber', 'AccountType',
                   'Balance', 'BankStatementText')

        writer.writerow(columns)
        accounts = IAccountList(self.context)
        for accountdict in accounts.list(date):
            account = accountdict.get('obj')
            row = []
            row.append(account.getId())
            row.append(account.Title())
            row.append(account.getAccountNumber())
            row.append(account.getAccountType())
            balance = accountdict.get('balance')
            if accountdict['iscredit']:
                balance = -balance
            row.append(balance)
            # join on comma since the csv importer knows how to handle
            # this.
            row.append(','.join(account.getBankStatementText()))
            writer.writerow(row)

        return output

