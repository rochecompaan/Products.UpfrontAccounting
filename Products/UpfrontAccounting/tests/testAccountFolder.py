# -*- coding: utf-8 -*-
#
# File: testAccountFolder.py
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

from Products.UpfrontAccounting.content.AccountFolder import AccountFolder
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.CMFCore.utils import getToolByName
import string


class testAccountFolder(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_generateUniqueId(self):
        portal = self.getPortal()
        id = 'upfrontbooks'
        ledger = portal[id].ledger
        accountfolder = ledger.accounts

        accountid = ledger.getAccountID()
        prefix = ledger.getAccountPrefix()
        id_str = "%s%s" % (prefix, string.zfill(str(accountid+1), 6))

        self.assertEqual(id_str, accountfolder.generateUniqueId('Account'))
        self.failUnless(accountfolder.generateUniqueId('Account') != \
                        accountfolder.generateUniqueId('Account'))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testAccountFolder))
    return suite

if __name__ == '__main__':
    framework()


