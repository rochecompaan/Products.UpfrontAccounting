import csv
from cStringIO import StringIO
from zope.interface import implements, Interface
from Products.Five import BrowserView
from DateTime import DateTime
from Products.UpfrontAccounting.interfaces import ICSVWriter
from Products.UpfrontAccounting.browser.listaccounttransactions import \
    ListAccountTransactionsView
from Products.UpfrontAccounting.adapters.transactioncsv import \
    getColumnHeadings

class IAccountTransactionExporter(Interface):
    """ Marker interface
    """

class AccountTransactionExporter(BrowserView):
    """ Export account transactions as CSV file
    """

    implements(IAccountTransactionExporter)

    def __call__(self):
        view = ListAccountTransactionsView(self.context, self.request)
        output = StringIO()
        writer = csv.writer(output)

        columns = ('title', 'TransactionDate', 'Debit', 'Credit', 'Balance')
        writer.writerow(columns)

        for entry in view.transactions(batch=False):
            row = []
            row.append(entry.Title())
            row.append(entry.getTransactionDate())
            if entry.getDebitCredit() == 'Debit':
                row.append(entry.getAmount())
                row.append('')
            elif entry.getDebitCredit() == 'Credit':
                row.append('')
                row.append(entry.getAmount())
            row.append(entry.balance)
            writer.writerow(row)

        filename = '%s_transactions.csv' % self.context.getId()

        output.seek(0)
        output = output.read()
        request = self.request
        request.RESPONSE.setHeader('Content-Type', 
            'text/comma-separated-values; charset=utf-8')
        request.RESPONSE.setHeader('Content-Disposition',
            'attachment; filename=%s' % filename)
        request.RESPONSE.setHeader('Content-Length', len(output))
        request.RESPONSE.setHeader('Cache-Control', 's-maxage=0')

        return output



