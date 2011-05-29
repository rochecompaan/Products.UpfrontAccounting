# -*- coding: utf-8 -*-
#
# File: CashBook.py
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
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.FinanceFields.Money import Money
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.CMFCore import permissions

##code-section module-header #fill in your manual code here
from zExceptions import NotFound
from zope.index.field import FieldIndex
from Products.FinanceFields.MoneyField import MoneyField
from Products.FinanceFields.MoneyWidget import MoneyWidget
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='BankAccount',
        vocabulary_factory="account_vocabulary",
        widget=ReferenceBrowserWidget(
            label="Bank Account",
            label_msgid='UpfrontAccounting_label_BankAccount',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary_display_path_bound=-1,
        relationship="CashBookBankAccount",
        default="",
        allowed_types=('Account',),
        required=True,
    ),
    LinesField(
        name='StripPhrasesFromImport',
        widget=LinesField._properties['widget'](
            label="Strip phrases from import",
            description="Phrases (one per line) will be stripped from the imported bank statement",
            label_msgid='UpfrontAccounting_label_StripPhrasesFromImport',
            description_msgid='UpfrontAccounting_help_StripPhrasesFromImport',
            i18n_domain='UpfrontAccounting',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CashBook_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CashBook(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICashBook)

    meta_type = 'CashBook'
    _at_rename_after_creation = True

    schema = CashBook_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(CashBook, PROJECTNAME)
# end of class CashBook

##code-section module-footer #fill in your manual code here
##/code-section module-footer



