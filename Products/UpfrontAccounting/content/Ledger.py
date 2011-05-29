# -*- coding: utf-8 -*-
#
# File: Ledger.py
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

# additional imports from tagged value 'import'
from Products.CMFCore import permissions
import string

##code-section module-header #fill in your manual code here
from threading import Lock
##/code-section module-header

schema = Schema((

    IntegerField(
        name='TransactionID',
        default=1,
        widget=IntegerField._properties['widget'](
            label="Transaction ID",
            label_msgid='UpfrontAccounting_label_TransactionID',
            i18n_domain='UpfrontAccounting',
        ),
        write_permission="UpfrontAccounting: ManageTransactionID",
    ),
    StringField(
        name='TransactionPrefix',
        default="T",
        widget=StringField._properties['widget'](
            size=5,
            label="Transaction Prefix",
            label_msgid='UpfrontAccounting_label_TransactionPrefix',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    IntegerField(
        name='AccountID',
        default=1,
        widget=IntegerField._properties['widget'](
            label="Account ID",
            label_msgid='UpfrontAccounting_label_AccountID',
            i18n_domain='UpfrontAccounting',
        ),
        write_permission="UpfrontAccounting: ManageAccountID",
    ),
    StringField(
        name='AccountPrefix',
        default="A",
        widget=StringField._properties['widget'](
            label="Account Prefix",
            size=5,
            label_msgid='UpfrontAccounting_label_AccountPrefix',
            i18n_domain='UpfrontAccounting',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Ledger_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
IdField = Ledger_schema['id']
IdField.widget.visible = {'edit':'hidden', 'view': 'invisible'}
TitleField = Ledger_schema['title']
TitleField.widget.visible = {'edit':'hidden', 'view': 'invisible'}
##/code-section after-schema

class Ledger(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ILedger)

    meta_type = 'Ledger'
    _at_rename_after_creation = True

    schema = Ledger_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def displayContentsTab(self):
        """ Hide contents tab
        """
        return False

    security.declareProtected(permissions.ModifyPortalContent, 'getNextTransactionId')
    def getNextTransactionId(self):
        # XXX: not thread safe, use Dieter's SharedResource
        id = self.getTransactionID()
        self.setTransactionID(id + 1)
        return "%s%s" % (self.getTransactionPrefix(),
                         string.zfill(str(id), 6))
    security.declareProtected(permissions.ModifyPortalContent,    'getNextAccountId')
    def getNextAccountId(self):
        lock = Lock()
        try:
            lock.acquire()
            id_num = self.getAccountID() + 1
            id_str = "%s%s" % (self.getAccountPrefix(),
                               string.zfill(str(id_num), 6))
            while id_str in self.keys():
                id_num += 1
                id_str = "%s%s" % (self.getAccountPrefix(),
                                   string.zfill(str(id_num), 6))
            self.setAccountID(id_num)
            return id_str
        finally:
            lock.release()

    security.declareProtected(permissions.View, 'getLedger')
    def getLedger(self):
        return self



registerType(Ledger, PROJECTNAME)
# end of class Ledger

##code-section module-footer #fill in your manual code here
##/code-section module-footer



