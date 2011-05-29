import csv
from cStringIO import StringIO

from zope.interface import implements
from zope.component import adapts

from Products.UpfrontAccounting.interfaces import ICSVWriter
from Products.UpfrontAccounting.content.interfaces import ITransaction

class TransactionCSVWriter(object):

    implements(ICSVWriter)

    adapts(ITransaction)

    def __init__(self, context):
        self.context = context
        self.request = context.request

    def write(self):
        """ Return account balances for a given date as CSV file. We
            return a StringIO instance to allow streaming of the output if
            required.
        """
        output = StringIO()
        writer = csv.writer(output)
        transaction = self.context
        writer.writerow(getColumnHeadings())
        writeCSVEntriesFromTransaction(writer, transaction)

        return output

def getColumnHeadings():
    """ return column headings for a transaction csv export
    """
    columns = ('id', 'title', 'effectiveDate', 'Account',
        'AccountTitle', 'AccountNumber', 'Amount', 'DebitCredit')
    return columns

def writeCSVEntriesFromTransaction(csvwriter, transaction):
    """ returns a list of rows with contents for each entry of a transaction
    """
    entries = transaction.objectValues()
    for entry in entries:
        __traceback_info__ = (transaction.getId(),)
        row = []
        row.append(transaction.getId())
        row.append(transaction.Title())
        row.append(transaction.getEffectiveDate().Date())

        account = entry.getAccount()
        row.append(account.getId())
        row.append(account.Title())
        row.append(account.getAccountNumber())
        
        row.append(entry.getAmount())
        row.append(entry.getDebitCredit())

        csvwriter.writerow(row)
