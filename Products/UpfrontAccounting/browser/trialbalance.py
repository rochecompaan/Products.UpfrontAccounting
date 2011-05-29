from DateTime import DateTime
from Products.Five import BrowserView
from zope.interface import implements, Interface
from Products.UpfrontAccounting.interfaces import IAccountList

class ITrialBalance(Interface):
    """ Marker interface
    """


class TrialBalance(BrowserView):

    implements(ITrialBalance)

    def name(self):
        return self.__name__

    def accounts(self):
        """ Return the accounts and their balances for a given date.
        """
        date = self.trial_balance_date()
        return IAccountList(self.context.ledger.accounts).list(date)

    def default_date(self):
        """ Compute the default date
        """
        # get the last closing date and add 365 days
        if self.context.getClosingDates():
            date = DateTime(self.context.getClosingDates().maxKey()) + 365
            year = date.year()
            leap = year%4==0 and (year%100!=0 or year%400==0)
            # add another day if this is a leap year
            if leap:
                date += 1
            date = date.Date()
        else:
            date = DateTime().Date()

        return date

    def trial_balance_date(self):
        if self.request.has_key('trial_balance_date'):
            date = DateTime(self.request.get('trial_balance_date'))
        else:
            date = DateTime()
        return date

    def trial_balance_date_formatted(self):
        return self.trial_balance_date().strftime('%d %b %Y')
