# -*- coding: utf-8 -*-
#
# File: CustomerAccountFolder.py
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
from Products.UpfrontAccounting.content.SubsidiaryAccountFolder import SubsidiaryAccountFolder
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

CustomerAccountFolder_schema = BaseFolderSchema.copy() + \
    getattr(SubsidiaryAccountFolder, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CustomerAccountFolder(BaseFolder, SubsidiaryAccountFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICustomerAccountFolder)

    meta_type = 'CustomerAccountFolder'
    _at_rename_after_creation = True

    schema = CustomerAccountFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.View, 'getAccountForCustomer')
    def getAccountForCustomer(self, customer):
        """ Find account for customer
        """
        for account in self.objectValues('CustomerAccount'):
            if account.getOrganisation().UID() == customer.UID():
                return account

    security.declareProtected(permissions.ModifyPortalContent, 'createAccountForCustomer')
    def createAccountForCustomer(self, customer):
        """ Create account for customer
        """
        account_id = self.generateUniqueId('CustomerAccount')
        self.invokeFactory(id=account_id, type_name='CustomerAccount')
        account = self._getOb(account_id)
        account.edit(Organisation=customer, title=customer.Title())
        return account



registerType(CustomerAccountFolder, PROJECTNAME)
# end of class CustomerAccountFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



