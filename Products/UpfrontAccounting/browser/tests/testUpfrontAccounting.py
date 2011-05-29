# -*- coding: utf-8 -*-
#
# File: testUpfrontAccounting.py
#
# Copyright (c) 2009 by Upfront Systems
# Generator: ArchGenXML 
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Upfront Systems <info@upfrontsystems.co.za>"""
__docformat__ = 'plaintext'

#
# Base TestCase for UpfrontAccounting
#

import os, sys, code
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.UpfrontAccounting.config import PRODUCT_DEPENDENCIES
from Products.UpfrontAccounting.config import DEPENDENCIES

# Add common dependencies
DEPENDENCIES.append('Archetypes')
PRODUCT_DEPENDENCIES.append('MimetypesRegistry')
PRODUCT_DEPENDENCIES.append('PortalTransforms')
PRODUCT_DEPENDENCIES.append('UpfrontAccounting')

# Install all (product-) dependencies, install them too
for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
    ZopeTestCase.installProduct(dependency)

ZopeTestCase.installProduct('UpfrontAccounting')

PRODUCTS = list()
PRODUCTS += DEPENDENCIES
PRODUCTS.append('UpfrontAccounting')

testcase = PloneTestCase.PloneTestCase
##code-section module-before-plone-site-setup #fill in your manual code here
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.FinanceFields.config import CURRENCY_DISPLAY_LIST
from Testing.ZopeTestCase import installProduct
installProduct('ZCatalog', 1)
##/code-section module-before-plone-site-setup

PloneTestCase.setupPloneSite(products=PRODUCTS)

class testUpfrontAccounting(testcase):
    """Base TestCase for UpfrontAccounting."""

    ##code-section class-header_testUpfrontAccounting #fill in your manual code here
    ##/code-section class-header_testUpfrontAccounting

    # Commented out for now, it gets blasted at the moment anyway.
    # Place it in the protected section if you need it.
    #def afterSetup(self):
    #    """
    #    """
    #    pass

    def _afterSetup(self):
        """
        """
        self.setRoles(('Manager',))
        portal = self.getPortal()
        portal.error_log._ignored_exceptions = ()

        portal_url = portal.absolute_url()

        id = 'upfrontbooks'

        upfrontbooks = AccountingFolder(id, id=id,
            AccountingCurrency=CURRENCY_DISPLAY_LIST[0])

        upfrontbooks.setAccountingCurrency(CURRENCY_DISPLAY_LIST[0])

        rval = portal._setObject(id, upfrontbooks)
        newid = isinstance(rval, basestring) and rval or id

        upfrontbooks = portal._getOb(newid)

    def interact(self, locals=None):
        """Provides an interactive shell aka console inside your testcase.

        It looks exact like in a doctestcase and you can copy and paste
        code from the shell into your doctest. The locals in the testcase are
        available, becasue you are in the testcase.

        In your testcase or doctest you can invoke the shell at any point by
        calling::

            >>> self.interact( locals() )

        locals -- passed to InteractiveInterpreter.__init__()
        """
        savestdout = sys.stdout
        sys.stdout = sys.stderr
        sys.stderr.write('='*70)
        console = code.InteractiveConsole(locals)
        console.interact("""
ZopeTestCase Interactive Console
(c) BlueDynamics Alliance, Austria - 2005

Note: You have the same locals available as in your test-case.
""")
        sys.stdout.write('\nend of ZopeTestCase Interactive Console session\n')
        sys.stdout.write('='*70+'\n')
        sys.stdout = savestdout


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testUpfrontAccounting))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()


