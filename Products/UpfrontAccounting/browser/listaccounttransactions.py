from Products.Five import BrowserView
from Products.CMFPlone.PloneBatch import Batch
from DateTime import DateTime

class ListAccountTransactionsView(BrowserView):
    """
    """

    def name(self):
        return self.__name__

    def transactions(self, batch=True):
        """
        """
        entries = self.context.getTransactionEntriesAndBalances()

        if self.request.has_key('start_date'):
            startdate = DateTime(self.request.get('start_date'))
            enddate = DateTime(self.request.get('end_date'))

            # XXX: needs to be indexed and optimised
            entries = [e for e in entries \
                       if e.getTransactionDate() >= startdate and \
                       e.getTransactionDate() <= enddate]


        b_size = self.request.get('b_size', 100)
        b_start = self.request.get('b_start', (len(entries)/100) * 100)
        if batch:
            return Batch(entries, b_size, int(b_start), orphan=1)
        else:
            return entries

