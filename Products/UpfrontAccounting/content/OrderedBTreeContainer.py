# -*- coding: utf-8 -*-
#
# File: OrderedBTreeContainer.py
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
from BTrees.IOBTree import IOBTree
from BTrees.OIBTree import OIBTree
from Products.CMFCore import permissions

##code-section module-header #fill in your manual code here
from DocumentTemplate.sequence import sort
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

OrderedBTreeContainer_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class OrderedBTreeContainer(BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IOrderedBTreeContainer)

    meta_type = 'OrderedBTreeContainer'
    _at_rename_after_creation = True

    schema = OrderedBTreeContainer_schema

    ##code-section class-header #fill in your manual code here

    # Methods

    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePrivate('_insert')
    def _insert(self, pos, id):
        """
        """
        positionId = self._positionId
        idPosition = self._idPosition
        # check if it is not inserted yet
        if positionId.insert(pos, id):
            idPosition[id] = pos
            return

        # create a gap in the list
        self._delta(pos, pos+1)

        # assign position and id
        positionId[pos] = id
        idPosition[id] = pos

    security.declarePrivate('_delete')
    def _delete(self, pos):
        """
        """
        positionId = self._positionId
        idPosition = self._idPosition
        if pos is None:
            return
        if len(positionId) <= 0:
            return
        if len(positionId) == 1:
            id = positionId[pos]
            del positionId[pos]
            del idPosition[id]
            return
        self._delta(pos, pos+1)

    security.declarePrivate('_moveObject')
    def _moveObject(self, id, position):
        """ Move id to position
            Does not check if position is sane
        """
        if position < 0:
            position = 0

        obj_pos = self.getObjectPosition(id)
        if obj_pos == position:
            return

        self._delete(obj_pos)
        self._insert(position, id)

    security.declarePrivate('__init__')
    def __init__(self, oid, **kwargs):
        self._positionId = IOBTree()
        self._idPosition = OIBTree()

    security.declarePrivate('_delta')
    def _delta(self, pos1, pos2):
        """ in the _positionId btree, move either creates a gap or shifts a
            portion left
        """
        if pos1 == pos2: return
        #assert(abs(pos1-pos2) == 1) # haven't implemented delta completely yet
        positionId = self._positionId
        idPosition = self._idPosition
        max = 0
        if len(positionId) > 1:
            max = positionId.maxKey()
        else:
            return
        if pos1 < pos2:
            # move left, ie, shortens list, that is, move left from pos2 to
            # pos1
            delIds = []
            for i in range(pos1, pos2):
                delIds.append(positionId[i])
            for i in range(pos1, max-(pos2-pos1)+1):
                idPosition[positionId[i+pos2-pos1]] = i
                positionId[i] = positionId[pos2+i-pos1]
            # clear out ids and positions no longer used
            for id in delIds:
                del idPosition[id]
            for i in range(max-(pos2-pos1)+1, max+1):
                del positionId[i]
        else:
            # create a gap, that is, lengthens the list, move right from pos1
            # to pos2, and shift the rest right
            for i in range(max+abs(pos1-pos2), pos2-1, -1):
                idPosition[positionId[i-abs(pos1-pos2)]] = i
                positionId[i] = positionId[i-abs(pos1-pos2)]
            for i in range(pos2, pos1+1):
                del positionId[i]

    security.declareProtected(permissions.ModifyPortalContent, 'getObjectPosition')
    def getObjectPosition(self, id):
        """ Get the object position for a given id
        """
        if id is not None and self._idPosition.has_key(id):
            return self._idPosition[id]
        return None

    security.declareProtected(permissions.ModifyPortalContent, 'getIdsInOrder')
    def getIdsInOrder(self, start, end):
        """ return a list of ids starting at start and ending at end
            if end is None or greater than the end, the list is truncated
            en start is None or less than 0 it is set to 0
            the ids is a list of length(end-start)
        """
        ids = []
        endIds = end
        # check if the tree is empty and if the list is wrapped
        if len(self._positionId) > 0 and (end is None or end < 0):
            endIds = self._positionId.maxKey()
        elif len(self._positionId) == 0:
            return []

        if start is None or start < 0:
            start = 0
        for i in range(start, endIds+1):
            if self._positionId.has_key(i):
                ids.append(self._positionId[i])
            else:
                break

        if end is None:
            return ids
        return ids[:end-start]

    security.declareProtected(permissions.ModifyPortalContent, 'getObjectId')
    def getObjectId(self, position):
        """
        """
        if position is not None and self._positionId.has_key(position):
            return self._positionId[position]
        return None

    security.declareProtected(permissions.ModifyPortalContent, 'moveObjectsUp')
    def moveObjectsUp(self, ids, delta=1, RESPONSE=None):
        """ Move an object up """

        if type(ids) is StringType:
            ids = (ids,)

        for id in ids:
            self._moveObject(id, self.getObjectPosition(id)-delta)

        if RESPONSE is not None:
            RESPONSE.redirect('manage_workspace')

    security.declareProtected(permissions.ModifyPortalContent, 'moveObjectsDown')
    def moveObjectsDown(self, ids, delta=1, RESPONSE=None):
        """ move an object down """

        if type(ids) is StringType:
            ids = (ids,)

        for id in ids:
            self._moveObject(id, self.getObjectPosition(id)+delta)

        if RESPONSE is not None:
            RESPONSE.redirect('manage_workspace')

    security.declareProtected(permissions.ModifyPortalContent, 'moveObjectsToTop')
    def moveObjectsToTop(self, ids, RESPONSE=None):
        """ move an object to the top """

        if type(ids) is StringType:
            ids = (ids,)

        i = 0
        while i < len(ids):
            self._moveObject(ids[i], i)
            i = i + 1

        if RESPONSE is not None:
            RESPONSE.redirect('manage_workspace')

    security.declareProtected(permissions.ModifyPortalContent, 'moveObjectsToBottom')
    def moveObjectsToBottom(self, ids, RESPONSE=None):
        """ move an object to the bottom """

        if type(ids) is StringType:
            ids = (ids,)

        i = 0
        max = self._positionId.maxKey()
        length = len(ids)
        while i < length:
            self._moveObject(ids[i], max - (length - 1)  + i)
            i += 1

        if RESPONSE is not None:
            RESPONSE.redirect('manage_workspace')

    security.declareProtected(permissions.ModifyPortalContent, 'orderObjects')
    def orderObjects(self, key, reverse=None):
        """ Order sub-objects by key and direction.
        """
        ids = [ id for id, obj in sort( self.objectItems(),
                                        ( (key, 'cmp', 'asc'), ) ) ]
        if reverse:
            ids.reverse()

        self._clear_and_rebuild(ids=ids)
        return len(ids)

    security.declareProtected(permissions.ModifyPortalContent, 'moveObjectsByDelta')
    def moveObjectsByDelta(self, ids, delta, subset_ids=None):
        """ Move specified sub-objects by delta.
        """
        raise "Not implemented yet"
        if type(ids) is StringType:
            ids = (ids,)
        min_position = 0
        objects = list(self._objects)
        if subset_ids == None:
            # OLD: subset_ids = [ obj['id'] for obj in objects ]
            subset_ids = self.getCMFObjectsSubsetIds(objects)
        else:
            subset_ids = list(subset_ids)
        # unify moving direction
        if delta > 0:
            ids = list(ids)
            ids.reverse()
            subset_ids.reverse()
        counter = 0

        for id in ids:
            try:
                old_position = subset_ids.index(id)
            except ValueError:
                continue
            new_position = max( old_position - abs(delta), min_position )
            if new_position == min_position:
                min_position += 1
            if not old_position == new_position:
                subset_ids.remove(id)
                subset_ids.insert(new_position, id)
                counter += 1

        if counter > 0:
            if delta > 0:
                subset_ids.reverse()
            obj_dict = {}
            for obj in objects:
                obj_dict[ obj['id'] ] = obj
            pos = 0
            for i in range( len(objects) ):
                if objects[i]['id'] in subset_ids:
                    try:
                        objects[i] = obj_dict[ subset_ids[pos] ]
                        pos += 1
                    except KeyError:
                        raise ValueError('The object with the id "%s" does '
                                         'not exist.' % subset_ids[pos])
            self._objects = tuple(objects)

        return counter

    security.declareProtected(permissions.ModifyPortalContent, 'getFirstEntryId')
    def getFirstEntryId(self):
        """
        """
        if len(self._positionId) > 0:
            return self._positionId[self._positionId.minKey()]
        return None

    security.declareProtected(permissions.ModifyPortalContent, 'getLastEntryId')
    def getLastEntryId(self):
        """
        """
        if len(self._positionId) > 0:
            return self._positionId[self._positionId.maxKey()]
        return None

    def addObject(self, id):
        """Adds object to end of btree, returns position
        """
        if self.getObjectPosition(id) is not None:
            raise RuntimeError, "Object already in tree"

        if len(self._positionId) > 0:
            max = self._positionId.maxKey()
            self._positionId[max+1] = id
            self._idPosition[id] = max + 1
            return max + 1
        else:
            self._positionId[0] = id
            self._idPosition[id] = 0
            return 0

    def numberObjects(self):
        """
        """
        return len(self._positionId)

    security.declarePrivate('_clear_and_rebuild')
    def _clear_and_rebuild(self, ids=[]):
        """
        """
        self._positionId = IOBTree()
        self._idPosition = OIBTree()

        for id in ids:
            self.addObject(id)



# end of class OrderedBTreeContainer

##code-section module-footer #fill in your manual code here
##/code-section module-footer



