# -*- coding: utf-8 -*-
#
# File: CreditNoteFolder.py
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
from Products.CMFCore import permissions
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CreditNoteFolder_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CreditNoteFolder(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICreditNoteFolder)

    meta_type = 'CreditNoteFolder'
    _at_rename_after_creation = True

    schema = CreditNoteFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.ModifyPortalContent, 'generateUniqueId')
    def generateUniqueId(self, type_name='CreditNote'):
        """
        """
        return str(self.getNextCreditNoteNumber())



registerType(CreditNoteFolder, PROJECTNAME)
# end of class CreditNoteFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



