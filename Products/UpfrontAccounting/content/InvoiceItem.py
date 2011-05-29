# -*- coding: utf-8 -*-
#
# File: InvoiceItem.py
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
from Products.FinanceFields.FixedPointField import FixedPointField
from Products.FinanceFields.Money import Money

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    FixedPointField(
        name='Quantity',
        default='0.0',
        widget=FixedPointField._properties['widget'](
            label='Quantity',
            label_msgid='UpfrontAccounting_label_Quantity',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),
    StringField(
        name='Unit',
        widget=StringField._properties['widget'](
            label='Unit',
            label_msgid='UpfrontAccounting_label_Unit',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    MoneyField(
        name='Rate',
        widget=MoneyField._properties['widget'](
            label='Rate',
            label_msgid='UpfrontAccounting_label_Rate',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
        default_currency_method="getInvoiceCurrency",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

InvoiceItem_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class InvoiceItem(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IInvoiceItem)

    meta_type = 'InvoiceItem'
    _at_rename_after_creation = True

    schema = InvoiceItem_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(ManageInvoices, 'getTotal')
    def getTotal(self):
        """ Calculate the item total """
        u, q = self.getRate(), self.getQuantity()
        if u and q:
            return u * q
        else:
            return Money('0.00', self.getInvoiceCurrency())



registerType(InvoiceItem, PROJECTNAME)
# end of class InvoiceItem

##code-section module-footer #fill in your manual code here
##/code-section module-footer



