# -*- coding: utf-8 -*-
#
# File: SubsidiaryLedger.py
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
from Products.UpfrontAccounting.content.Ledger import Ledger
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.UpfrontAccounting.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore import permissions
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='ControlAccount',
        widget=ReferenceWidget(
            label="Control Account",
            label_msgid='UpfrontAccounting_label_ControlAccount',
            i18n_domain='UpfrontAccounting',
        ),
        allowed_types=('Account',),
        vocabulary_display_path_bound=-1,
        relationship="SubsidiaryLedgerControlAccount",
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SubsidiaryLedger_schema = BaseSchema.copy() + \
    getattr(Ledger, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class SubsidiaryLedger(BaseContent, Ledger, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ISubsidiaryLedger)

    meta_type = 'SubsidiaryLedger'
    _at_rename_after_creation = True

    schema = SubsidiaryLedger_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declareProtected(permissions.ModifyPortalContent, 'setControlAccount')
    def setControlAccount(self, value, **kw):
        """ The control account will only be set upon creation.
        """
        current_account = self.getControlAccount()
        if current_account:
            if current_account.UID() == value[0]:
                return
            else:
                raise RuntimeError(CannotModifyControlAccount)
        if not value:
            return
        field = self.Schema().get('ControlAccount')
        field.set(self, value, **kw)

        # let the control account know that this ledger is the
        # subsidiary ledger
        account = self.getControlAccount()
        account.setSubsidiaryLedger(self.UID())

    security.declareProtected(permissions.View, 'isSubsidiaryLedger')
    def isSubsidiaryLedger(self):
        """ Assert that we are in the context of a SubsidiaryLedger.
        """
        return True



registerType(SubsidiaryLedger, PROJECTNAME)
# end of class SubsidiaryLedger

##code-section module-footer #fill in your manual code here
##/code-section module-footer



