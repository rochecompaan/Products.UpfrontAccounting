# -*- coding: utf-8 -*-
#
# File: AccountingFolder.py
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
from Products.FinanceFields.FixedPointField import FixedPointField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.FinanceFields.config import CURRENCY_DISPLAY_LIST
from Products.CMFCore import permissions

##code-section module-header #fill in your manual code here
from BTrees.IIBTree import IISet
from DateTime import DateTime
from organisationschema import organisation_schema
##/code-section module-header

schema = Schema((

    StringField(
        name='AccountingCurrency',
        widget=SelectionWidget(
            label="Accounting Currency",
            description="The currency that should be used to store all monetary values. Transactions in other currencies will be converted to this currency for accounting purposes.",
            visible="{'edit':'hidden', 'view': 'visible'}",
            label_msgid='UpfrontAccounting_label_AccountingCurrency',
            description_msgid='UpfrontAccounting_help_AccountingCurrency',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
        vocabulary=CURRENCY_DISPLAY_LIST,
    ),
    FixedPointField(
        name='SalesTaxPercentage',
        default='0.0',
        widget=FixedPointField._properties['widget'](
            label="Sales Tax Percentage",
            label_msgid='UpfrontAccounting_label_SalesTaxPercentage',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),
    ReferenceField(
        name='DefaultSalesAccount',
        vocabulary_factory="account_vocabulary",
        widget=ReferenceWidget(
            label="Default Sales Account",
            description="The account that should be used when invoicing clients.",
            label_msgid='UpfrontAccounting_label_DefaultSalesAccount',
            description_msgid='UpfrontAccounting_help_DefaultSalesAccount',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary_display_path_bound=-1,
        relationship="AccountingFolderDefaultSalesAccount",
        allowed_types=('Account',),
        required=True,
    ),
    ReferenceField(
        name='SalesTaxAccount',
        vocabulary_factory="account_vocabulary",
        widget=ReferenceWidget(
            label="Sales Tax Account",
            description="The tax account that should be used when invoicing clients.",
            label_msgid='UpfrontAccounting_label_SalesTaxAccount',
            description_msgid='UpfrontAccounting_help_SalesTaxAccount',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary_display_path_bound=-1,
        relationship="AccountingFolderSalesTaxAccount",
        allowed_types=('Account',),
        required=True,
    ),
    ReferenceField(
        name='RetainedIncomeAccount',
        vocabulary_factory="account_vocabulary",
        widget=ReferenceWidget(
            label="Retained income account",
            description="The account that should be used to record end of year profit and losses.",
            label_msgid='UpfrontAccounting_label_RetainedIncomeAccount',
            description_msgid='UpfrontAccounting_help_RetainedIncomeAccount',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary_display_path_bound=-1,
        relationship="AccountingFolderRetainedIncome",
        allowed_types=('Account',),
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

AccountingFolder_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
AccountingFolder_schema = AccountingFolder_schema.copy() + \
    organisation_schema.copy()

# delete organisation name from schema
del AccountingFolder_schema['OrganisationName']
##/code-section after-schema

class AccountingFolder(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IAccountingFolder)

    meta_type = 'AccountingFolder'
    _at_rename_after_creation = True

    schema = AccountingFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def __init__(self, oid, **kwargs):
        BaseFolder.__init__(self, oid, **kwargs)
        self._closing_transfers = IISet()

    security.declareProtected(permissions.View, 'getAccountingRoot')
    def getAccountingRoot(self):
        ''' Return 'self' as accounting root
        '''
        return self

    def displayContentsTab(self):
        """ Hide contents tab
        """
        return False

    def registerClosingDate(self, date):
        """ register closing transfer date
        """
        # strip time before insert
        date = int(DateTime(date.Date()))
        self._closing_transfers.insert(date)

    def getClosingDates(self):
        """ return all registered closing dates
        """
        return self._closing_transfers



registerType(AccountingFolder, PROJECTNAME)
# end of class AccountingFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



