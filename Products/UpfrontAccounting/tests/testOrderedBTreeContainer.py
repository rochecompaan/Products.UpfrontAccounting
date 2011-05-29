# -*- coding: utf-8 -*-
#
# File: testOrderedBTreeContainer.py
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

from Products.UpfrontAccounting.content.OrderedBTreeContainer import \
        OrderedBTreeContainer
from Products.FinanceFields.Money import Money
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.UpfrontAccounting.content.AccountingFolder import \
        AccountingFolder
from Products.UpfrontAccounting.content.interfaces import \
        IOrderedBTreeContainer
from zope.interface import providedBy


class testOrderedBTreeContainer(testUpfrontAccounting):
    """Test-cases for class(es) ."""

    def test_getLastEntryId(self):
        obtree = self._create_obtree_container()
        self.failUnless(isinstance(obtree, OrderedBTreeContainer))

        self.failUnless(obtree.getLastEntryId() is None)

        id0 = 'dummy0'
        pos0 = obtree.addObject(id0)

        self.failUnless(obtree.getLastEntryId() == id0)

        id1 = 'dummy1'
        pos1 = obtree.addObject(id1)

        self.failUnless(obtree.getLastEntryId() == id1)

        id2 = 'dummy2'
        pos2 = obtree.addObject(id2)

        self.failUnless(obtree.getLastEntryId() == id2)

    def test_getObjectId(self):
        obtree = self._create_obtree_container()
        self.failUnless(isinstance(obtree, OrderedBTreeContainer))

        self.failUnless(obtree.getObjectId(None) is None)

        id0 = 'dummy0'
        pos0 = obtree.addObject(id0)

        self.failUnless(id0 == obtree.getObjectId(pos0))

        id1 = 'dummy1'
        pos1 = obtree.addObject(id1)

        self.failUnless(id1 == obtree.getObjectId(pos1))

        id2 = 'dummy2'
        pos2 = obtree.addObject(id2)

        self.failUnless(id2 == obtree.getObjectId(pos2))

        id3 = 'dummy3'
        pos3 = obtree.addObject(id3)

        self.failUnless(id3 == obtree.getObjectId(pos3))

        # random

        self.failUnless(id1 == obtree.getObjectId(pos1))
        self.failUnless(id0 == obtree.getObjectId(pos0))
        self.failUnless(id3 == obtree.getObjectId(pos3))

        self.failUnless(obtree.getObjectId(None) is None)
        self.failUnless(obtree.getObjectId(-1) is None)

    def test_getFirstEntryId(self):
        obtree = self._create_obtree_container()
        self.failUnless(isinstance(obtree, OrderedBTreeContainer))

        self.failUnless(obtree.getFirstEntryId() is None)

        # check for correct position
        id0 = 'dummy0'
        pos0 = obtree.addObject(id0)

        self.failUnless(obtree.getFirstEntryId() == id0)

        id1 = 'dummy1'
        pos1 = obtree.addObject(id1)

        self.failUnless(obtree.getFirstEntryId() == id0)

        id2 = 'dummy2'
        pos2 = obtree.addObject(id2)

        self.failUnless(obtree.getFirstEntryId() == id0)

    def test_getIdsInOrder(self):
        obtree = self._create_obtree_container()
        self.failUnless(isinstance(obtree, OrderedBTreeContainer))

        self.failUnless(len(obtree.getIdsInOrder(0,0)) == 0)
        self.failUnless(len(obtree.getIdsInOrder(0,10)) == 0)
        self.failUnless(len(obtree.getIdsInOrder(-1,10)) == 0)

        id0 = 'dummy0'
        pos0 = obtree.addObject(id0)

        id1 = 'dummy1'
        pos1 = obtree.addObject(id1)

        id2 = 'dummy2'
        pos1 = obtree.addObject(id2)

        id3 = 'dummy3'
        pos1 = obtree.addObject(id3)

        ids = obtree.getIdsInOrder(0,4)

        self.failUnless(len(ids) == 4)

        for i in range(4):
            self.failUnless(ids[i] == 'dummy%s' % i)

        ids = obtree.getIdsInOrder(0,10)

        self.failUnless(len(ids) == 4)

        for i in range(4):
            self.failUnless(ids[i] == 'dummy%s' % i)

        ids = obtree.getIdsInOrder(-10,10)

        self.failUnless(len(ids) == 4)

        for i in range(4):
            self.failUnless(ids[i] == 'dummy%s' % i)

        ids = obtree.getIdsInOrder(1,3)

        self.failUnless(len(ids) == 2)

        for i in range(1,3):
            self.failUnless(ids[i-1] == 'dummy%s' % i)

    def test_instantiation(self):
        obtree = self._create_obtree_container()
        self.failUnless(isinstance(obtree, OrderedBTreeContainer))

    def _create_obtree_container(self):
        return OrderedBTreeContainer('obtreecontainer')

    def test_orderObjects(self):
        id = 'upfrontbooks'
        books = getattr(self.getPortal(), id)
        # the cashbook subclasses the ordredbtreecontainer

        cashbook = books.cashbook

        # no objects to order, use a dummy key
        self.failUnless(IOrderedBTreeContainer.providedBy(cashbook.entries))
        self.assertEqual(cashbook.orderObjects('dummy', reverse=False), 0)

        ids = [id for id in cashbook.entries.objectIds()]
        for id in ids:
            cashbook.entries._delObject(id)
        cashbook.entries._id_counter = 0

        for i in range(1,5):
            self._add_cashbookentry(5-i)

        ids = cashbook.entries.getIdsInOrder(0, None)
        self.assertEqual(len(ids), 4)

        cashbook.orderObjects('getAmount', reverse=False)
        orderedIds = cashbook.entries.getIdsInOrder(0, None)

        self.assertEqual(len(orderedIds), 4)

        orderedIds.reverse()
        self.assertEqual(orderedIds[0], '000004')
        self.assertEqual(orderedIds[1], '000003')
        self.assertEqual(orderedIds[2], '000002')
        self.assertEqual(orderedIds[3], '000001')

        cashbook.orderObjects('getAmount', reverse=True)
        orderedIds = cashbook.entries.getIdsInOrder(0, None)
        self.assertEqual(orderedIds[0], '000001')
        self.assertEqual(orderedIds[1], '000002')
        self.assertEqual(orderedIds[2], '000003')
        self.assertEqual(orderedIds[3], '000004')

    def test_addObject(self):
        obtree = self._create_obtree_container()
        self.failUnless(isinstance(obtree, OrderedBTreeContainer))

        self.failUnless(obtree.getLastEntryId() is None)

        for i in range(5):
            id = 'dummy%s' % i
            pos = obtree.addObject(id)
            self.failUnless(pos == i)

        self.failUnless(obtree.getFirstEntryId() == 'dummy0')
        self.failUnless(obtree.getLastEntryId() == 'dummy4')
        self.failUnless(len(obtree.getIdsInOrder(0, None)) == 5)

    def test_numberObjects(self):
        obtree = self._create_obtree_container()
        self.failUnless(isinstance(obtree, OrderedBTreeContainer))

        self.failUnless(obtree.numberObjects() == 0)

        for i in range(5):
            id = 'dummy%s' % i
            pos = obtree.addObject(id)

        self.failUnless(obtree.numberObjects() == 5)

    def test_getObjectPosition(self):
        obtree = self._create_obtree_container()
        self.failUnless(isinstance(obtree, OrderedBTreeContainer))

        # check edge case
        self.failUnless(obtree.getObjectPosition(None) is None)

        # check for correct position
        id0 = 'dummy0'
        pos0 = obtree.addObject(id0)
        self.failUnless(pos0 is not None)
        self.failUnless(obtree.getObjectPosition(id0) is not None)
        self.failUnless(obtree.getObjectPosition(id0) == pos0)

        id1 = 'dummy1'
        pos1 = obtree.addObject(id1)
        self.failUnless(pos1 is not None)
        self.failUnless(obtree.getObjectPosition(id1) is not None)
        self.failUnless(obtree.getObjectPosition(id1) == pos1)
        self.failUnless(pos0 != pos1)

        self.failUnless(obtree.getObjectPosition(id0) == pos0)

        # check order
        self.failUnless(pos0 < pos1)

        self.failUnless(obtree.getObjectPosition('dummy2') is None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testOrderedBTreeContainer))
    return suite

if __name__ == '__main__':
    framework()


