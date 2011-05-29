# -*- coding: utf-8 -*-
#
# File: Invoice.py
#
# Copyright (c) 2010 by Upfront Systems
# Generator: ArchGenXML 
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Upfront Systems <info@upfrontsystems.co.za>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.UpfrontAccounting.config import *

# additional imports from tagged value 'import'
from Products.FinanceFields.config import CURRENCY_DISPLAY_LIST
from Products.FinanceFields.FixedPointField import FixedPointField
from Products.FinanceFields.Money import Money

##code-section module-header #fill in your manual code here
import string
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='Quote',
        widget=ReferenceWidget(
            checkbox_bound=-1,
            description="If you select a quote then the invoice will automatically be created from the quote.",
            label='Quote',
            label_msgid='UpfrontAccounting_label_Quote',
            description_msgid='UpfrontAccounting_help_Quote',
            i18n_domain='UpfrontAccounting',
        ),
        allowed_types=('Quote',),
        relationship="InvoiceQuote",
    ),
    ReferenceField(
        name='CustomerAccount',
        vocabulary_factory="custaccount_vocabulary",
        widget=ReferenceWidget(
            checkbox_bound=-1,
            label="Customer Account",
            label_msgid='UpfrontAccounting_label_CustomerAccount',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary_display_path_bound=-1,
        relationship="InvoiceCustomerAccount",
        required=True,
        allowed_types="CustomerAccount",
    ),
    DateTimeField(
        name='InvoiceDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            label="Invoice Date",
            label_msgid='UpfrontAccounting_label_InvoiceDate',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),
    BooleanField(
        name='CalculateTax',
        default="True",
        widget=BooleanField._properties['widget'](
            label="Calculate Tax",
            description="Sales tax is calculated additionally.",
            label_msgid='UpfrontAccounting_label_CalculateTax',
            description_msgid='UpfrontAccounting_help_CalculateTax',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    StringField(
        name='InvoiceCurrency',
        widget=SelectionWidget(
            label="Invoice Currency",
            label_msgid='UpfrontAccounting_label_InvoiceCurrency',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
        vocabulary=CURRENCY_DISPLAY_LIST,
    ),
    FixedPointField(
        name='ExchangeRate',
        default='1.0',
        widget=FixedPointField._properties['widget'](
            label="Exchange Rate",
            description="Specify the exchange rate if the invoice currency differs from the accounting currency.",
            label_msgid='UpfrontAccounting_label_ExchangeRate',
            description_msgid='UpfrontAccounting_help_ExchangeRate',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),
    TextField(
        name='Notes',
        widget=TextAreaWidget(
            label='Notes',
            label_msgid='UpfrontAccounting_label_Notes',
            i18n_domain='UpfrontAccounting',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Invoice_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Invoice_schema['title'].default_method = 'getId'
##/code-section after-schema

class Invoice(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IInvoice)

    meta_type = 'Invoice'
    _at_rename_after_creation = True

    schema = Invoice_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def __init__(self, oid, **kwargs):
        BaseFolder.__init__(self, oid, **kwargs)
        self._id_counter = 0

    security.declareProtected(ModifyPortalContent, 'generateUniqueId')
    def generateUniqueId(self, type_name):
        """ return the next id for invoice items
        """
        self._id_counter += 1
        return string.zfill(self._id_counter, 3)

    security.declareProtected(ManageInvoices, 'getSubTotal')
    def getSubTotal(self):
        total = Money('0.00', self.getInvoiceCurrency())
        for item in self.objectValues('InvoiceItem'):
            total += item.getTotal()
        return total

    security.declareProtected(ManageInvoices, 'getTotal')
    def getTotal(self):
        tax = 0
        if self.getCalculateTax():
            tax = self.getSalesTaxPercentage()
        st = self.getSubTotal()
        return st + (st * tax / 100)

    security.declareProtected(ManageInvoices, 'getTaxAmount')
    def getTaxAmount(self):
        return self.getTotal() - self.getSubTotal()

    security.declareProtected(ManageInvoices, 'getConvertedSubTotal')
    def getConvertedSubTotal(self):
        amount = self.getSubTotal().amount() * self.getExchangeRate()
        return Money(amount, self.getAccountingCurrency())

    security.declareProtected(ManageInvoices, 'getConvertedTotal')
    def getConvertedTotal(self):
        amount = self.getTotal().amount() * self.getExchangeRate()
        return Money(amount, self.getAccountingCurrency())

    security.declareProtected(ManageInvoices, 'getConvertedTaxAmount')
    def getConvertedTaxAmount(self):
        amount = self.getTaxAmount().amount() * self.getExchangeRate()
        return Money(amount, self.getAccountingCurrency())

    security.declareProtected(ModifyPortalContent, 'review_state')
    def review_state(self):
        portal_workflow = getToolByName(self, 'portal_workflow')
        return portal_workflow.getInfoFor(self, 'review_state')

    security.declareProtected(ModifyPortalContent, 'reindexObject')
    def reindexObject(self, idxs=[]):
        """ index object in invoice_catalog
        """
        self.invoice_catalog.catalog_object(self)



registerType(Invoice, PROJECTNAME)
# end of class Invoice

##code-section module-footer #fill in your manual code here
##/code-section module-footer



