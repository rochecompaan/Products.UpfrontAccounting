from zope.interface import implements, Interface
from plone.app.content.browser.foldercontents import FolderContentsTable
from zope.schema.interfaces import IVocabularyFactory
from DateTime import DateTime

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.FinanceFields.Money import Money
from Products.UpfrontAccounting.interfaces import IAccountTotal
from zope.schema.vocabulary import SimpleVocabulary
from textwrap import wrap

class IAccountTotalView(Interface):
    """ Marker interface
    """

class IZeroMoneyInstance(Interface):
    """ Marker interface
    """

class IListAccounts(Interface):
    """ Marker interface
    """

class IWrapText(Interface):
    """ Marker interface
    """
    
    def wrap_text(text, columns=80, indent=0):
        """ returns wrapped text
        """

class IAccountAutoComplete(Interface):
    """ Interface for AccountAutoComplete browser view
    """

    def items():
        """ render the items used by javascript autocomplete widget
        """

    def js(id):
        """ render the javascript to enable autocomplete on given DOM id
        """

class AccountTotal(BrowserView):

    implements(IAccountTotalView)

    def _get_date(self):
        """ Get the date from the request
        """
        date = self.request.get('filter_date')
        if date:
            date = DateTime(date)
        else:
            date = DateTime()
        return date

    def total(self):
        """ Compute the total for all balances
        """
        date = self._get_date()
        return IAccountTotal(self.context).getTotal(date)

    def debit_total(self):
        """ Compute the total for debit balances
        """
        date = self._get_date()
        return IAccountTotal(self.context).getDebitTotal(date)

    def credit_total(self):
        """ Compute the total for credit balances
        """
        date = self._get_date()
        return IAccountTotal(self.context).getCreditTotal(date)


class ZeroMoneyInstance(BrowserView):

    implements(IZeroMoneyInstance)

    def __call__(self):
        return Money('0.00', self.context.getAccountingCurrency())

class WrapText(BrowserView):

    implements(IWrapText)

    def wrap_text(self, text, columns=80, indent=0):

        if type(text) == type(u''):
            text = text.encode(self.context.getSiteEncoding())

        lst = []
        for l in text.split('\n'):
            lst.extend(wrap(l, columns))

        if indent:
            for i in range(len(lst)):
                lst[i] = (' '*int(indent)) + lst[i]

        return '\n'.join(lst)

class ListAccounts(BrowserView):
    """ Return a list of accounts for a given accounting folder
    """

    implements(IListAccounts)

    def list(self, accounttype=None):
        root = self.context.getAccountingRoot()
        pc = getToolByName(self.context, 'portal_catalog')
        portal_types = []
        if accounttype is None or accounttype == 'Ledger':
            portal_types.append('Account')
        if accounttype is None or accounttype == 'Customer':
            portal_types.append('CustomerAccount')
        if accounttype is None or accounttype == 'Supplier':
            portal_types.append('SupplierAccount')

        accounts = [p.getObject() for p in pc(portal_type=portal_types,
                                              sort_on='sortable_title')]
        return accounts

class AccountAutoComplete(BrowserView):
    """ Return javascript for Account Auto Complete widget
    """

    implements(IAccountAutoComplete)

    def items(self):
        options = []

        view = ListAccounts(self.context, self.request)
        uidmap = {}
        for account in view.list():
            option = "%s (%s)" % (
                account.Title(), account.getLedger().Title())
            options.append(option)
            uidmap[option] = account.UID()

        return """
        var items = "%(items)s".split(",");
        var uidmap = %(uidmap)s;
        function formatResult(row) {
            return row[0].replace(/^(.*)\s\(.+?\)$/, '$1');
        }
        """ % dict(items=','.join(options), uidmap=str(uidmap))

    def js(self, id):
        return """
        (function($) {
            $().ready(function() {
                $('#%(id)s').autocomplete(items, {
                    formatResult: formatResult
                    });
            });
        })(jQuery);
        """ % dict(id=id)


class FolderButtons(BrowserView):
    """ Make the buttons defined in the FolderContentsTable available to
        other templates.
    """

    def buttons(self):
        table = FolderContentsTable(self.context, self.request)
        return table.buttons

class OrganisationLogo(BrowserView):
    """ Make organisation logo available to PDF template
    """

    def logo(self):
        return self.context.Logo.index_html(self.request, self.request.RESPONSE)

    def width(self):
        field = self.context.Schema().get('Logo')
        width, height = field.getSize(self.context)
        # downsizing with a factor of 2.5 seems accurate for PDF
        return width / 2.5

    def height(self):
        field = self.context.Schema().get('Logo')
        width, height = field.getSize(self.context)
        return height / 2.5


class Vocabulary(object):
    """ Generate a vocabulary limited to the accounting root
        If no field is specified, use 'Account' as source for the vocabulary
    """
    implements(IVocabularyFactory)

    def __init__(self, field=None):
        self.field = field

    def __call__(self, context):
        root = context.getAccountingRoot()
        pc = getToolByName(context, 'portal_catalog')
        allowed_types = self.field and \
            context.schema[self.field].allowed_types or ('Account',)
        brains = pc(
            path='/'.join(root.getPhysicalPath()),
            meta_type=allowed_types,
            sort_on='sortable_title',
            )
        items = [(brain.Title, brain.UID) for brain in brains]
        return SimpleVocabulary.fromItems(items)

DefaultAccountVocabularyFactory = Vocabulary()
# if the fields should be specific, use these:
TransactionEntryAccountVocabularyFactory = Vocabulary(field='Account')
CustomerAccountVocabularyFactory = Vocabulary(field='CustomerAccount')
CashbookEntryAccountVocabularyFactory = Vocabulary(field='Account')

DefaultSalesAccountVocabularyFactory = Vocabulary(field='DefaultSalesAccount')
SalesTaxAccountFactory = Vocabulary(field='SalesTaxAccount')
RetainedIncomeAccountFactory = Vocabulary(field='RetainedIncomeAccount')
