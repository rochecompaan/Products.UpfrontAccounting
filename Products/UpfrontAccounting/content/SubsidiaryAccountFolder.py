# -*- coding: utf-8 -*-
#
# File: SubsidiaryAccountFolder.py
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
from Products.UpfrontAccounting.content.AccountFolder import AccountFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.UpfrontAccounting.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SubsidiaryAccountFolder_schema = BaseFolderSchema.copy() + \
    getattr(AccountFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class SubsidiaryAccountFolder(BaseFolder, AccountFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISubsidiaryAccountFolder)

    meta_type = 'SubsidiaryAccountFolder'
    _at_rename_after_creation = True

    schema = SubsidiaryAccountFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(SubsidiaryAccountFolder, PROJECTNAME)
# end of class SubsidiaryAccountFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



