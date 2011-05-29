from zope import interface, schema
from zope.formlib import form
from zope.component import queryUtility

from plone.i18n.normalizer.interfaces import IIDNormalizer

from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase
from Products.FinanceFields.config import CURRENCY_DISPLAY_LIST
from Products.UpfrontAccounting.config import COUNTRY_NAMES
from Products.UpfrontAccounting.content.AccountingFolder import \
    AccountingFolder

class IAccountingFolder(interface.Interface):
    OrganisationName = schema.TextLine(
        title=u'Organisation',
        description=u'The name of the organisation the accounts are for',
        required=True)
    AccountingCurrency = schema.Choice(
        title=u'Accounting Currency',
        required=True,
        description=u'The base currency for your accounts',
        values=CURRENCY_DISPLAY_LIST.sortedByValue().values()
        ) 
    Email = schema.TextLine(
        title=u'Organisation Email',
        description=u'Organisation email address',
        required=False)
    TaxNumber = schema.TextLine(
        title=u'Tax Number',
        description=u'Tax Number',
        required=False)
    Phone = schema.TextLine(
        title=u'Phone',
        description=u'Organisation phone number',
        required=False)
    Fax = schema.TextLine(
        title=u'Fax',
        description=u'Organisation fax number',
        required=False)
    Address = schema.Text(
        title=u'Billing Address',
        description=u'Addres that will appear on invoices and statements',
        required=False)
    City = schema.TextLine(
        title=u'City',
        required=False)
    PostalCode = schema.TextLine(
        title=u'Postal Code',
        required=False)
    Country = schema.Choice(
        title=u'Country',
        required=False,
        values=COUNTRY_NAMES)

class AccountingFolderAddForm(formbase.PageAddForm):
    """ We use a custom add form for the AccountingFolder since adding
        using portal_factory is not compatible with the way that we
        boostrap the hierarchy of accounts after object creation.
    """

    form_fields = form.FormFields(IAccountingFolder)

    def create(self, data):
        title = data['OrganisationName']
        data['title'] = title
        id = queryUtility(IIDNormalizer).normalize(title)
        self.contentName = id

        folder = AccountingFolder(id, title=title)
        # wrap the folder to allow edits
        folder = folder.__of__(self.context)
        folder.edit(**data)
        return folder

    def nextURL(self):
        obj = self.context.get(self.contentName)
        return "%s/view" % obj.absolute_url()

    def setUpWidgets(self, ignore_request=False):
        super(AccountingFolderAddForm, self).setUpWidgets(ignore_request)

        # limit size for address widget
        self.widgets.get('Address').width = 50
        self.widgets.get('Address').height = 5
