# -*- coding: utf-8 -*-
#
# File: Transaction.py
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
from Products.FinanceFields.Money import Money

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ModifyPortalContent, View
import string
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
from Products.CMFCore import permissions
##/code-section after-local-schema

Transaction_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
effective = Transaction_schema['effectiveDate']
effective.required = True
effective.widget.label = 'Transaction Date'
effective.widget.description = ''
effective.widget.show_hm = False
##/code-section after-schema

class Transaction(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ITransaction)

    meta_type = 'Transaction'
    _at_rename_after_creation = False

    schema = Transaction_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def __init__(self, oid, **kwargs):
        BaseFolder.__init__(self, oid, **kwargs)
        self._id_counter = 0

    security.declareProtected(ModifyPortalContent, 'generateUniqueId')
    def generateUniqueId(self, type_name):
        """ return the next id for transaction entries
        """
        self._id_counter += 1
        return string.zfill(self._id_counter, 3)

    security.declareProtected(View, 'folder_contents')
    def folder_contents(self):
        """ Redirect to view """
        self.REQUEST.RESPONSE.redirect('view')

    security.declareProtected(View, 'entries')
    def entries(self):
        return self.objectValues('TransactionEntry')

    security.declareProtected(View, 'getDebitTotal')
    def getDebitTotal(self):
        return self.getTotalForSign(DEBIT)

    security.declareProtected(View, 'getCreditTotal')
    def getCreditTotal(self):
        return self.getTotalForSign(CREDIT)

    security.declareProtected(View, 'getTotalForSign')
    def getTotalForSign(self, sign):
        total = Money('0.0', self.getAccountingCurrency())
        for entry in self.objectValues(('TransactionEntry',
                'SubsidiaryTransactionEntry')):
            if entry.getDebitCredit() == sign:
                total = total + entry.getAmount()
        return total

    security.declareProtected(View, 'getTotalForSign')
    def getTotal(self):
        """ Compute total for transaction """
        return self.getDebitTotal() - self.getCreditTotal()

    security.declareProtected(ModifyPortalContent, 'reindexObject')
    def reindexObject(self, idxs=[]):
        """ index object in transaction_catalog
        """
        self.transaction_catalog.catalog_object(self)

    security.declareProtected(ModifyPortalContent, 'reindexObjectSecurity')
    def reindexObjectSecurity(self, skip_self=False):
        """ We don't index object security on a transaction
        """
        return

    security.declareProtected(View, 'review_state')
    def review_state(self):
        """ return review_state
        """
        wftool = getToolByName(self, 'portal_workflow')
        return wftool.getInfoFor(self, 'review_state', None)

    security.declareProtected(View, 'canPostTransaction')
    def canPostTransaction(self):
        return self.getTotal() == 0 and len(self.entries()) > 0

    security.declareProtected(View, 'canUndoOrReverse')
    def canUndoOrReverse(self):
        """ Used by the undo and reverse transaction method attributes.
            A member can undo or reverse a transaction if the
            transaction is not in the posted state and if the member has
            the ModifyPortalContent permission on the transaction
            folder.
        """
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        has_permission = member.has_permission(
            ModifyPortalContent, self.getTransactionFolder())
        return has_permission and self.review_state() == 'posted'



registerType(Transaction, PROJECTNAME)
# end of class Transaction

##code-section module-footer #fill in your manual code here
##/code-section module-footer



