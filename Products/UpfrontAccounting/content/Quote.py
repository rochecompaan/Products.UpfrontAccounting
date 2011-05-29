# -*- coding: utf-8 -*-
#
# File: Quote.py
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
from Products.UpfrontAccounting.content.Invoice import Invoice
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.UpfrontAccounting.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='Customer',
        widget=ReferenceWidget(
            checkbox_bound=-1,
            label="Customer",
            label_msgid='UpfrontAccounting_label_Customer',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary_display_path_bound=-1,
        allowed_types=('CustomerAccount',),
        relationship="QuoteCustomer",
        required=True,
    ),
    DateTimeField(
        name='QuoteDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            label="Quote Date",
            label_msgid='UpfrontAccounting_label_QuoteDate',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Quote_schema = BaseFolderSchema.copy() + \
    getattr(Invoice, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
del Quote_schema['Quote']
del Quote_schema['InvoiceDate']
del Quote_schema['CustomerAccount']
Quote_schema['InvoiceCurrency'].widget.label = 'Quote currency'
Quote_schema['InvoiceCurrency'].widget.label_msgid = \
    'UpfrontAccounting_label_QuoteCurrency'
##/code-section after-schema

class Quote(BaseFolder, Invoice, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IQuote)

    meta_type = 'Quote'
    _at_rename_after_creation = True

    schema = Quote_schema

    ##code-section class-header #fill in your manual code here
    getQuote = None
    getInvoiceDate = None
    getCustomerAccount = None
    ##/code-section class-header

    # Methods


registerType(Quote, PROJECTNAME)
# end of class Quote

##code-section module-footer #fill in your manual code here
##/code-section module-footer



