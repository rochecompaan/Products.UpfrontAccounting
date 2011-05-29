from zope.interface import Interface

class IAccountingCurrency(Interface):
    """ Marker interface
    """

class IAccountTotal(Interface):

    def getTotal():
        """ Get the accounting currency for the site
        """

class IDebitTotal(Interface):
    """ Marker interface for an object that gives the total for all
        debit amounts in a sequence.
    """

class ICreditTotal(Interface):
    """ Marker interface for an object that gives the total for all
        credit amounts in a sequence.
    """

class IAccountList(Interface):

    def list():
        """ prepare a listing of accounts with debit and credit balances
            for a given date.
        """

class ICreditNoteList(Interface):
    """ interface for creditnotelist browser view
    """

class ICSVWriter(Interface):

    def write():
        """ Generate CSV file 
        """

class IZeroMoneyInstance(Interface):
    """ Marker interface
    """

class ICurrency(Interface):
    """ Marker interface
    """

class IThemeSpecific(Interface):
    """ Marker interface
    """

class ICashbookView(Interface):
     """Marker interface identifying Cashbook View.

     """

class ICashBookEntry(Interface):
    """ Marker interface
    """

class IMail(Interface):
    """ Interface for mailing view """

    def send(mail):
        """ Mail a mail
        """

class IMailInvoice(IMail):
    """ Marker interface for mailing invoices """

class IMailStatement(IMail):
    """ Marker interface for mailing statements """

