# -*- coding: utf-8 -*-
#
# File: CreditNote.py
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
from Products.FinanceFields.MoneyField import MoneyField

##code-section module-header #fill in your manual code here
from Products.FinanceFields.Money import Money
from Products.CMFCore import permissions
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='CustomerAccount',
        widget=ReferenceWidget(
            checkbox_bound=-1,
            label="Customer Account",
            label_msgid='UpfrontAccounting_label_CustomerAccount',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary_display_path_bound=-1,
        allowed_types=('CustomerAccount',),
        relationship="CreditNoteCustomerAccount",
        required=True,
    ),
    ReferenceField(
        name='SalesAccount',
        widget=ReferenceWidget(
            label="Sales Account",
            label_msgid='UpfrontAccounting_label_SalesAccount',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary_display_path_bound=-1,
        relationship="CreditNoteSalesAccount",
        default_method="getDefaultSalesAccount",
        required=True,
        allowed_types=('Account',),
    ),
    DateTimeField(
        name='CreditNoteDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            label="Credit Note Date",
            label_msgid='UpfrontAccounting_label_CreditNoteDate',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),
    MoneyField(
        name='Amount',
        widget=MoneyField._properties['widget'](
            label='Amount',
            label_msgid='UpfrontAccounting_label_Amount',
            i18n_domain='UpfrontAccounting',
        ),
        required=False,
    ),
    BooleanField(
        name='CalculateTax',
        default="True",
        widget=BooleanField._properties['widget'](
            label="Calculate Tax",
            description="The amount excludes sales tax and tax must be calculated additionally.",
            label_msgid='UpfrontAccounting_label_CalculateTax',
            description_msgid='UpfrontAccounting_help_CalculateTax',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    FixedPointField(
        name='ExchangeRate',
        default="1.0",
        widget=FixedPointField._properties['widget'](
            label="Exchange Rate",
            description="Specify the exchange rate if the credit note currency differs from the accounting currency.",
            label_msgid='UpfrontAccounting_label_ExchangeRate',
            description_msgid='UpfrontAccounting_help_ExchangeRate',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CreditNote_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CreditNote(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICreditNote)

    meta_type = 'CreditNote'
    _at_rename_after_creation = True

    schema = CreditNote_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.View, 'getTaxAmount')
    def getTaxAmount(self):
        zeroMoneyInstance = Money('0.0', self.getAccountingCurrency())
        if not self.getCalculateTax():
            return zeroMoneyInstance
        amount = self.getAmount()
        if not amount:
            amount = zeroMoneyInstance
        return self.getTotal() - amount

    security.declareProtected(permissions.View, 'getTotal')
    def getTotal(self):
        """ return 0 for now
        """
        tax = 0
        if self.getCalculateTax():
            tax = self.getSalesTaxPercentage()
        amount = self.getAmount()
        if not amount:
            amount = self.getZeroMoneyInstance()
        return amount + (amount * tax / 100)

    security.declareProtected(permissions.View, 'getCustomerAccountTitle')
    def getCustomerAccountTitle(self):
        """ Return Account Title
        """
        account = self.getCustomerAccount()
        if account:
            return str(account.Title())
        else:
            return ""



registerType(CreditNote, PROJECTNAME)
# end of class CreditNote

##code-section module-footer #fill in your manual code here
##/code-section module-footer



