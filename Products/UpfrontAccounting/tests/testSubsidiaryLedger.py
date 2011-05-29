# -*- coding: utf-8 -*-
#
# File: testSubsidiaryLedger.py
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

from Products.UpfrontAccounting.content.SubsidiaryLedger import \
        SubsidiaryLedger
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.content.AccountFolder import \
        AccountFolder
from Products.CMFCore.utils import getToolByName
from zope.event import notify
from DateTime import DateTime
from Products.UpfrontAccounting.content.interfaces import ISubsidiaryLedger


class testSubsidiaryLedger(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_setControlAccount(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        books = getattr(portal, id)

        ledger = getattr(books, 'ledger')
        accounts = getattr(ledger, 'accounts')
        self.failUnless(isinstance(accounts, AccountFolder))

        subsidiaryLedger = getattr(books, 'receivables')

        self.failUnless(ISubsidiaryLedger.providedBy(subsidiaryLedger))
        control = subsidiaryLedger.getControlAccount()

        self.failUnless(control)

        acc = None
        for acc in accounts.objectValues():
            if acc != control:
                break

        self.failUnless(acc is not None)

        self.assertRaises(RuntimeError, 
                          subsidiaryLedger.setControlAccount,
                          acc.UID())

        self.failUnless(control.getSubsidiaryLedger() == subsidiaryLedger)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSubsidiaryLedger))
    return suite

if __name__ == '__main__':
    framework()


