# -*- coding: utf-8 -*-
#
# File: InvoiceTemplate.py
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


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

InvoiceTemplate_schema = BaseFolderSchema.copy() + \
    getattr(Invoice, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class InvoiceTemplate(BaseFolder, Invoice, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IInvoiceTemplate)

    meta_type = 'InvoiceTemplate'
    _at_rename_after_creation = True

    schema = InvoiceTemplate_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def __init__(self, oid, **kwargs):
        BaseFolder.__init__(self, oid, **kwargs)
        self._id_counter = 0



registerType(InvoiceTemplate, PROJECTNAME)
# end of class InvoiceTemplate

##code-section module-footer #fill in your manual code here
##/code-section module-footer



