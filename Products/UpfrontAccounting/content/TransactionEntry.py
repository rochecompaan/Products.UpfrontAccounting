# -*- coding: utf-8 -*-
#
# File: TransactionEntry.py
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
from Products.FinanceFields.MoneyWidget import MoneyWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.SimpleReferenceField.SimpleReferenceField import SimpleReferenceField

##code-section module-header #fill in your manual code here
from Products.CMFCore import permissions

##/code-section module-header

schema = Schema((

    SimpleReferenceField(
        name='Account',
        vocabulary_factory="tentry_account_vocabulary",
        widget=SimpleReferenceField._properties['widget'](
            label='Account',
            label_msgid='UpfrontAccounting_label_Account',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
        relationship="TransactionEntryAccount",
        allowed_types=('Account', 'CustomerAccount', 'SupplierAccount'),
        storage=AnnotationStorage(),
    ),
    StringField(
        name='DebitCredit',
        widget=StringField._properties['widget'](
            label="Debit/Credit",
            label_msgid='UpfrontAccounting_label_DebitCredit',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
        vocabulary=(DEBIT, CREDIT),
    ),
    MoneyField(
        name='Amount',
        mutator="editAmount",
        widget=MoneyWidget(
            label='Amount',
            label_msgid='UpfrontAccounting_label_Amount',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TransactionEntry_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TransactionEntry(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ITransactionEntry)

    meta_type = 'TransactionEntry'
    _at_rename_after_creation = True

    schema = TransactionEntry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.View, 'getURL')
    def getURL(self, relative=False):
        """
        """
        return self.absolute_url()

    security.declareProtected(permissions.ModifyPortalContent, 'editAmount')
    def editAmount(self, value):
        """ Set Amount
        """
        if value is None:
            return
        if False: #value < 0:
            msg = self.translate("value_must_be_positive",
                domain='UpfrontAccounting',
                default='Value must be a positive number'
                )
            raise ValueError, (msg, `value`)
        field = self.Schema()['Amount']
        field.set(self, value)

    security.declareProtected(permissions.ModifyPortalContent, 'post')
    def post(self):
        """
        Add a reference to this entry from the Account
        """
        account = self.getAccount()
        if self.getDebitCredit() == DEBIT:
            account.debitAccount(self.getAmount(),
                                 self.getTransactionDate())
        elif self.getDebitCredit() == CREDIT:
            account.creditAccount(self.getAmount(),
                                  self.getTransactionDate())
        field = account.Schema()['TransactionEntries']
        res = field.getRaw(account)
        if res is None:
            value = [self.UID()]
        else:
            value = res + [self.UID()]
        account.setTransactionEntries(value)

    security.declareProtected(permissions.ModifyPortalContent, 'removeTransactionEntryFromAccount')
    def removeTransactionEntryFromAccount(self):
        """ remove a transaction entry from account
        """
        # undo the debit/credit part
        account = self.getAccount()
        if self.getDebitCredit() == DEBIT:
            account.creditAccount(self.getAmount(),
                                 self.getTransactionDate())
        elif self.getDebitCredit() == CREDIT:
            account.debitAccount(self.getAmount(),
                                  self.getTransactionDate())
        # remove the reference
        field = account.Schema()['TransactionEntries']
        res = field.getRaw(account)
        if res is not None:
            value = [r for r in res if r != self.UID()]
        account.setTransactionEntries(value)

    security.declareProtected(permissions.View, 'getTransactionDate')
    def getTransactionDate(self):
        if getattr(self, 'aq_parent', None):
            return self.aq_parent.getEffectiveDate()
        else:
            return None

    security.declareProtected(permissions.View, 'Title')
    def Title(self):
        if getattr(self, 'aq_parent', None):
            return self.aq_parent.Title()
        else:
            return self.getId()



registerType(TransactionEntry, PROJECTNAME)
# end of class TransactionEntry

##code-section module-footer #fill in your manual code here
##/code-section module-footer



