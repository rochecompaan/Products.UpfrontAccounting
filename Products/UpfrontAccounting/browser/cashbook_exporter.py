import csv
from cStringIO import StringIO
from zope.interface import implements, Interface
from Products.Five import BrowserView
from DateTime import DateTime
from Products.UpfrontAccounting.interfaces import ICSVWriter

class ICashbookExporter(Interface):
    """ Marker interface
    """

class CashbookExporter(BrowserView):
    """ Export cashbook entries as CSV file
    """

    implements(ICashbookExporter)

    def __call__(self):
        cashbook = self.context
        entries = cashbook.entries.entriesInOrder()

        output = StringIO()
        writer = csv.writer(output)

        columns = ('title', 'Date', 'ReferenceNumber', 'Account',
                    'AccountTitle', 'TaxIncluded', 'Amount', 'Balance')
        writer.writerow(columns)

        for entry in entries:
            row = []
            row.append(entry.Title())
            row.append(entry.getDate())
            row.append(entry.getReferenceNumber())

            account = entry.getAccount()
            row.append(account.getId())
            row.append(account.Title())
            row.append(entry.getTaxIncluded())
            row.append(entry.getAmount())
            row.append(cashbook.entries.getBalanceForEntry(entry.getId()))
            writer.writerow(row)

        filename = '%s_cashbookentries.csv' % cashbook.getAccountingRoot().getId()

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



