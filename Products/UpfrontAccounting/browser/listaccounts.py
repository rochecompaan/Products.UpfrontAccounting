from Products.Five import BrowserView
from zope.interface import implements, Interface
from DateTime import DateTime
from Products.UpfrontAccounting.interfaces import IAccountList

class ListAccountsView(BrowserView):

    def accounts(self):
        """ Return the accounts and their balances for a given date if
            specified.
        """
        date = DateTime()
        if self.request.has_key('filter_date'):
            date = DateTime(self.request.get('filter_date'))
        return IAccountList(self.context).list(date)

    def filter_date(self):
        date = self.request.get('filter_date', DateTime())
        return date
