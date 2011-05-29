# -*- coding: utf-8 -*-
#
# File: InvoiceFolder.py
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

##code-section module-header #fill in your manual code here
from Products.FinanceFields.Money import Money
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

InvoiceFolder_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class InvoiceFolder(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IInvoiceFolder)

    meta_type = 'InvoiceFolder'
    _at_rename_after_creation = True

    schema = InvoiceFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.ModifyPortalContent, 'generateUniqueId')
    def generateUniqueId(self, type_name):
        """
        """
        return str(self.getNextInvoiceNumber())

    security.declareProtected(permissions.View, 'getPendingInvoices')
    def getPendingInvoices(self):
        """ return all invoices in the pending state
        """
        invoices = []
        for brain in self.invoice_catalog(review_state='pending'):
            invoice = brain.getObject()
            invoices.append(invoice)
        return invoices

    def postPendingInvoices(self, REQUEST=None):
        """ post all the pending invoices
        """
        workflowTool = getToolByName(self, "portal_workflow")
        for invoice in self.getPendingInvoices():
            workflowTool.doActionFor(invoice, "post")



registerType(InvoiceFolder, PROJECTNAME)
# end of class InvoiceFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



