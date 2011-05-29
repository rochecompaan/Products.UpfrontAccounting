import csv
from cStringIO import StringIO

from zope.interface import implements
from zope.component import adapts

from Products.UpfrontAccounting.interfaces import ICSVWriter
from Products.UpfrontAccounting.content.interfaces import ITransactionFolder
from transactioncsv import getColumnHeadings, writeCSVEntriesFromTransaction

class TransactionFolderCSVWriter(object):

    implements(ICSVWriter)

    adapts(ITransactionFolder)

    def __init__(self, context):
        self.context = context
        self.request = context.request

    def _genContentFilter(self):
        request = self.request
        start_date = request.get('getTransactionDate_from')
        end_date = request.get('getTransactionDate_to')
        if start_date and end_date:
            content_filter = {
                'sort_on': 'effective',
                'effective': {'query': [start_date, end_date], 
                'range': 'min:max'}
                }
        else:
            content_filter = {
                'sort_on': 'effective',
                }
        
        return content_filter

    def _genTransactionList(self):
        return self.context.transaction_catalog(self._genContentFilter())

    def write(self):
        """ Return transactions for a given date as CSV file. We return 
            a StringIO instance to allow streaming of the output if
            required.
        """
        output = StringIO()
        writer = csv.writer(output)
        transactionfolder = self.context

        writer.writerow(getColumnHeadings())

        transactions = self._genTransactionList()
        for transactionBrain in transactions:
            transaction = transactionBrain.getObject()
            writeCSVEntriesFromTransaction(writer, transaction)

        return output
