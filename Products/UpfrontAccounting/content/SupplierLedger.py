# -*- coding: utf-8 -*-
#
# File: SupplierLedger.py
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
from Products.UpfrontAccounting.content.CustomerLedger import CustomerLedger
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.UpfrontAccounting.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SupplierLedger_schema = BaseFolderSchema.copy() + \
    getattr(CustomerLedger, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class SupplierLedger(BaseFolder, CustomerLedger, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISupplierLedger)

    meta_type = 'SupplierLedger'
    _at_rename_after_creation = True

    schema = SupplierLedger_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(SupplierLedger, PROJECTNAME)
# end of class SupplierLedger

##code-section module-footer #fill in your manual code here
##/code-section module-footer



