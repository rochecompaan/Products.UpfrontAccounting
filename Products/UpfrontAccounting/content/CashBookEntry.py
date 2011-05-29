# -*- coding: utf-8 -*-
#
# File: CashBookEntry.py
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
from DateTime import DateTime
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
import sys
from Products.FinanceFields.MoneyField import MoneyField
from Products.FinanceFields.MoneyWidget import MoneyWidget
from Products.CMFCore import permissions
from upfront.simplereferenceField import SimpleReferenceField

##code-section module-header #fill in your manual code here
from Products.FinanceFields.Money import Money
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='Date',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            label='Date',
            label_msgid='UpfrontAccounting_label_Date',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    StringField(
        name='ReferenceNumber',
        widget=StringField._properties['widget'](
            label="Reference Number",
            label_msgid='UpfrontAccounting_label_ReferenceNumber',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    SimpleReferenceField(
        name='Account',
        vocabulary_factory="cb_entry_account_vocabulary",
        widget=SimpleReferenceField._properties['widget'](
            label='Account',
            label_msgid='UpfrontAccounting_label_Account',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary_display_path_bound=-1,
        relationship="CashBookEntryAccount",
        allowed_types=('Account', 'CustomerAccount', 'SupplierAccount'),
        storage=AnnotationStorage(),
        required=True,
    ),
    BooleanField(
        name='TaxIncluded',
        default="False",
        widget=BooleanField._properties['widget'](
            label="Tax Included",
            label_msgid='UpfrontAccounting_label_TaxIncluded',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    MoneyField(
        name='Amount',
        widget=MoneyWidget(
            label='Amount',
            label_msgid='UpfrontAccounting_label_Amount',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),
    StringField(
        name='AccountType',
        default="Ledger",
        widget=SelectionWidget(
            label="Account Type",
            label_msgid='UpfrontAccounting_label_AccountType',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary=('Ledger', 'Customer', 'Supplier'),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CashBookEntry_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CashBookEntry(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICashBookEntry)

    meta_type = 'CashBookEntry'
    _at_rename_after_creation = True

    schema = CashBookEntry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.View, 'isPosted')
    def isPosted(self):
        """ are we posted?
        """
        wftool = getToolByName(self, 'portal_workflow')
        return wftool.getInfoFor(self, 'review_state', None) == 'posted'

    security.declareProtected(permissions.ModifyPortalContent, 'reindexObject')
    def reindexObject(self, idxs=[]):
        """ index object in cashbook_catalog
        """
        self.cashbook_catalog.catalog_object(self)

    security.declareProtected(permissions.ModifyPortalContent, 'reindexObjectSecurity')
    def reindexObjectSecurity(self, skip_self=False):
        """ We don't index object security on a cashbook entry
        """
        return

    def review_state(self):
        """ lookup the entry's review_state
        """
        wftool = getToolByName(self, 'portal_workflow')
        return wftool.getInfoFor(self, 'review_state', None)

    security.declareProtected(permissions.View, 'canPost')
    def canPost(self):
        """ can we post?
        """
        wftool = getToolByName(self, 'portal_workflow')
        zeroMoneyInstance = Money('0.0', self.aq_parent.getAccountingCurrency())
        return self.getAmount() \
            and self.getAmount() != zeroMoneyInstance\
            and self.getAccount()\
            and self.getDate()\
            and self.aq_parent.getBankAccount()\
            and wftool.getInfoFor(self, 'review_state', None) == 'pending'
    security.declareProtected(permissions.ModifyPortalContent, 'setAmount')
    def setAmount(self, amount):
        """
        """
        oldVal = self.getAmount()
        amountField = self.schema.get('Amount')
        amount = amount or Money('0.00', self.aq_parent.getAccountingCurrency())
        amountField.set(self, amount)
        if oldVal is None:
            self.aq_parent.updateBalance(self.getId(), self.getAmount())
        else:
            self.aq_parent.removeEntryBalance(self.getId(), keepPosition=True)
            self.aq_parent.updateBalance(self.getId(), self.getAmount())

    security.declareProtected(permissions.View, 'Title')
    def Title(self):
        """
        """
        return self.getRawDescription()



registerType(CashBookEntry, PROJECTNAME)
# end of class CashBookEntry

##code-section module-footer #fill in your manual code here
##/code-section module-footer



