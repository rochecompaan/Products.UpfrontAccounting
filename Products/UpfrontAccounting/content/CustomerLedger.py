# -*- coding: utf-8 -*-
#
# File: CustomerLedger.py
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
from Products.UpfrontAccounting.content.SubsidiaryLedger import SubsidiaryLedger
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.UpfrontAccounting.config import *

# additional imports from tagged value 'import'
import string

##code-section module-header #fill in your manual code here
from Products.CMFCore import permissions
##/code-section module-header

schema = Schema((

    IntegerField(
        name='InvoiceNumber',
        default=1,
        widget=IntegerField._properties['widget'](
            label="Invoice Number",
            label_msgid='UpfrontAccounting_label_InvoiceNumber',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    StringField(
        name='InvoicePrefix',
        default="I",
        widget=StringField._properties['widget'](
            label="Invoice Prefix",
            label_msgid='UpfrontAccounting_label_InvoicePrefix',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    IntegerField(
        name='QuoteNumber',
        default=1,
        widget=IntegerField._properties['widget'](
            label="Quote Number",
            label_msgid='UpfrontAccounting_label_QuoteNumber',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    StringField(
        name='QuotePrefix',
        default="Q",
        widget=StringField._properties['widget'](
            label="Quote Prefix",
            label_msgid='UpfrontAccounting_label_QuotePrefix',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    IntegerField(
        name='CreditNoteNumber',
        default=1,
        widget=IntegerField._properties['widget'](
            label="Credit Note Number",
            label_msgid='UpfrontAccounting_label_CreditNoteNumber',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    StringField(
        name='CreditNotePrefix',
        default="CR",
        widget=StringField._properties['widget'](
            label="Credit Note Prefix",
            label_msgid='UpfrontAccounting_label_CreditNotePrefix',
            i18n_domain='UpfrontAccounting',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CustomerLedger_schema = BaseFolderSchema.copy() + \
    getattr(SubsidiaryLedger, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CustomerLedger(BaseFolder, SubsidiaryLedger, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICustomerLedger)

    meta_type = 'CustomerLedger'
    _at_rename_after_creation = True

    schema = CustomerLedger_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.View, 'isReceivable')
    def isReceivable(self):
        return self.getControlAccount().Type == 'Asset'

    security.declareProtected(permissions.View, 'isPayable')
    def isPayable(self):
        return self.getControlAccount().Type == 'Liability'

    security.declareProtected(permissions.ModifyPortalContent, 'getNextInvoiceNumber')
    def getNextInvoiceNumber(self):
        field = self.Schema().get('InvoiceNumber')
        nr = field.get(self)
        id = str(nr)
        field.set(self, nr+1)
        return "%s%s" % (self.getInvoicePrefix(), string.zfill(id, 6))

    security.declareProtected(permissions.ModifyPortalContent, 'getNextQuoteNumber')
    def getNextQuoteNumber(self):
        field = self.Schema().get('QuoteNumber')
        nr = field.get(self)
        id = str(nr)
        field.set(self, nr+1)
        return "%s%s" % (self.getQuotePrefix(), string.zfill(id, 6))

    security.declareProtected(permissions.ModifyPortalContent, 'getNextCreditNoteNumber')
    def getNextCreditNoteNumber(self):
        field = self.Schema().get('CreditNoteNumber')
        nr = field.get(self)
        id = str(nr)
        field.set(self, nr+1)
        return "%s%s" % (self.getCreditNotePrefix(), string.zfill(id, 6))



registerType(CustomerLedger, PROJECTNAME)
# end of class CustomerLedger

##code-section module-footer #fill in your manual code here
##/code-section module-footer



