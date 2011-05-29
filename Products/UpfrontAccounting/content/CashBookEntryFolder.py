# -*- coding: utf-8 -*-
#
# File: CashBookEntryFolder.py
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
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from OrderedBTreeContainer import OrderedBTreeContainer

##code-section module-header #fill in your manual code here
from BTrees.OOBTree import OOBTree
from Products.CMFCore.permissions import ModifyPortalContent, View
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CashBookEntryFolder_schema = BaseBTreeFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class CashBookEntryFolder(BaseBTreeFolder, OrderedBTreeContainer, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICashBookEntryFolder)

    meta_type = 'CashBookEntryFolder'
    _at_rename_after_creation = True

    schema = CashBookEntryFolder_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePrivate('__init__')
    def __init__(self, oid, **kwargs):
        BaseBTreeFolder.__init__(self, oid, **kwargs)
        self._balances = OOBTree()
        self._id_counter = 0
        OrderedBTreeContainer.__init__(self, oid, **kwargs)

    security.declareProtected(ModifyPortalContent, 'generateUniqueId')
    def generateUniqueId(self, type_name):
        """ return the next id for cashbook entries contained in this ob
        """
        self._id_counter += 1
        return '%06d' % (self._id_counter,)

    security.declareProtected(View, 'getEntriesLastAccount')
    def getEntriesLastAccount(self):
        """ returns the last account selected for cashbook entry, hopefully
            reduces UI input
        """
        id = self.getLastEntryId()
        if id:
            return self[id].getAccount()
        return None

    security.declareProtected(View, 'getBalanceForEntry')
    def getBalanceForEntry(self, entryId):
        """ returns the total in the cashbook or, if the date is not none, the
            total up to that day
        """
        balances = self._balances
        balance = balances.get(entryId,
            Money('0.00', self.getAccountingCurrency()))
        return balance

    security.declareProtected(ModifyPortalContent, 'removeEntryBalance')
    def removeEntryBalance(self, entryId, keepPosition=True):
        """ remove an entry from _balances
        """
        balances = self._balances
        diff = 0
        if balances.has_key(entryId):
            diff = self.prevBalance(entryId) - balances[entryId]
            del balances[entryId]

        # compute the total for all subsequent entries
        pos = self.getObjectPosition(entryId)
        # remove ob from OrderedContent
        if not keepPosition and pos is not None:
            self._delete(pos)
        elif pos is not None:
            pos = pos + 1
        while self.getObjectId(pos) is not None:
            id = self.getObjectId(pos)
            balances[id] = balances[id] + diff
            pos = pos + 1

    security.declareProtected(View, 'prevBalance')
    def prevBalance(self, entryId):
        """ return the previous balance
        """
        # get the previous balance
        balances = self._balances
        pos = self.getObjectPosition(entryId)

        # this may be the first entry
        if pos is None or pos == 0:
            return Money('0.00', self.getAccountingCurrency())

        pos = pos -1
        entry_id = self.getObjectId(pos)
        return self.getBalanceForEntry(entry_id)

    security.declareProtected(ModifyPortalContent, 'updateBalance')
    def updateBalance(self, entryId, amount):
        """ Update the balance of the cashbook. If amount is none, assume 0
        """
        amount = amount or Money('0.00', self.getAccountingCurrency())
        balances = self._balances
        curbalance = balances.get(entryId, None)
        # compute the total for all subsequent entries
        if curbalance is None:
            pos = self.getObjectPosition(entryId)
            if pos is not None:
                balances[entryId] = self.getBalanceForEntry(
                    self.getObjectId(pos-1)) + amount
                pos = pos + 1
                while pos < self.numberObjects():
                    id = self.getObjectId(pos)
                    balances[id] = balances[id] + amount
                    pos = pos + 1

            # add an entry at the bottom
            else:
                prevBalanceId = self.getObjectId(self.numberObjects() - 1)
                self.addObject(entryId)
                balances[entryId] = \
                    self.getBalanceForEntry(prevBalanceId) + amount

        # when an entries' value changes
        else:
            # not very efficient code, but so _elegant_ ...
            self.removeEntryBalance(entryId, keepPosition=True)
            self.updateBalance(entryId, amount)

    security.declareProtected(View, 'entriesInOrder')
    def entriesInOrder(self):
        """ return the entries in the order they are saved as
        """
        return [self[id] for id in self.getIdsInOrder(0, None)]

    security.declareProtected(View, 'getPendingEntries')
    def getPendingEntries(self):
        """ return all entries in the pending state
        """
        entries = []
        for brain in self.cashbook_catalog(review_state='pending'):
            entry = brain.getObject()
            entries.append((self.getObjectPosition(entry.getId()), entry))
        entries.sort()
        entries = [entry[1] for entry in entries]
        return entries

    security.declareProtected(ModifyPortalContent, 'postTransactions')
    def postTransactions(self, REQUEST=None):
        """ post all the pending cashbook entries
        """
        workflowTool = getToolByName(self, "portal_workflow")
        for entry in self.getPendingEntries():
            workflowTool.doActionFor(entry, "post")

        if REQUEST:
            REQUEST.RESPONSE.redirect(self.absolute_url())



registerType(CashBookEntryFolder, PROJECTNAME)
# end of class CashBookEntryFolder

##code-section module-footer #fill in your manual code here
##/code-section module-footer



