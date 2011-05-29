# -*- coding: utf-8 -*-
#
# File: testSubsidiaryAccountFolder.py
#
# Copyright (c) 2009 by Upfront Systems
# Generator: ArchGenXML 
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Upfront Systems <info@upfrontsystems.co.za>"""
__docformat__ = 'plaintext'

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.UpfrontAccounting.config import *
from Products.UpfrontAccounting.tests.testUpfrontAccounting import testUpfrontAccounting

from Products.UpfrontAccounting.content.CreditNoteFolder import \
        CreditNoteFolder
from Products.CMFCore.utils import getToolByName
from zope.interface import providedBy
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.Account import Account
from Products.UpfrontAccounting.content.AccountingFolder import \
    AccountingFolder
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from Products.UpfrontAccounting.content.interfaces import IAccount
from Products.UpfrontAccounting.config import DEBIT, CREDIT
from Products.FinanceFields.Money import Money
import StringIO, csv


class testListCreditNotesView(testUpfrontAccounting):
    """Test-cases for class(es) SubsidiaryAccountFolder."""

    # Manually created methods

    def _add_creditnote(self, amnt):
        creditnotes = self.accountingfolder.receivables.creditnotes
        new_id = creditnotes.generateUniqueId('CreditNote')
        typestool = getToolByName(self.getPortal(), 'portal_types')
        typestool.constructContent('CreditNote', creditnotes, new_id)
        creditnote = creditnotes[new_id]
        creditnote.edit(CreditNoteDate=DateTime().earliestTime(), Amount=amnt)
        return creditnotes[new_id]

    def test_batch(self):
        creditnotes = self.accountingfolder.receivables.creditnotes
        self.failUnless(isinstance(creditnotes, CreditNoteFolder))

        cnotes = []
        for i in range(0,2):
            amount = Money(i+13, self.accountingfolder.getAccountingCurrency())
            cnotes.append(self._add_creditnote(amount).getId())

        path = creditnotes.getPhysicalPath() + ('listcreditnotes',)

        creditnote_view = self.accountingfolder.restrictedTraverse(path)
        batch = creditnote_view.batch()

        self.failUnless(len(batch) == 2)
        self.failUnless(batch[0].id != batch[1].id)

        for e in batch:
            self.failUnless(e.id in cnotes)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testListCreditNotesView))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()




