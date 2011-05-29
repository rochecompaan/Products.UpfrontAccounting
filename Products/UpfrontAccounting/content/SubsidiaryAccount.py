# -*- coding: utf-8 -*-
#
# File: SubsidiaryAccount.py
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
from Products.UpfrontAccounting.content.Account import Account
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

SubsidiaryAccount_schema = BaseFolderSchema.copy() + \
    getattr(Account, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
AccountTypeField = SubsidiaryAccount_schema['AccountType']
AccountTypeField.required = 0 # This field is still required, but the
                              # mutator will ensure that value is set to
                              # the type of the control account

AccountTypeField.mutator = 'setAccountType'
AccountTypeField.widget.visible = {'edit': 'hidden', 'view': 'invisible'}
##/code-section after-schema

class SubsidiaryAccount(Account, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISubsidiaryAccount)

    meta_type = 'SubsidiaryAccount'
    _at_rename_after_creation = True

    schema = SubsidiaryAccount_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.ModifyPortalContent, 'setAccountType')
    def setAccountType(self, value, **kw_args):
        field = self.schema['AccountType']
        account = self.getControlAccount()
        if account:
            field.set(self, account.getAccountType())

    security.declareProtected(ManageTransactions, 'creditAccount')
    def creditAccount(self, amount, effective_date):
        """ extend inherited method to credit ourselves and the control
            account
        """
        Account.creditAccount(self, amount, effective_date)
        self.getControlAccount().creditAccount(amount, effective_date)

    security.declareProtected(ManageTransactions, 'debitAccount')
    def debitAccount(self, amount, effective_date):
        """ extend inherited method to debit ourselves and the control
            account
        """
        Account.debitAccount(self, amount, effective_date)
        self.getControlAccount().debitAccount(amount, effective_date)



registerType(SubsidiaryAccount, PROJECTNAME)
# end of class SubsidiaryAccount

##code-section module-footer #fill in your manual code here
##/code-section module-footer



