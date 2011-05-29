""" Run this script to add a review state index on CashBook
"""
import sys
import transaction
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from zope.index.field import FieldIndex
from zope.app.container.contained import ObjectAddedEvent
from zope.event import notify

try:
    portal_id = sys.argv[1]
except IndexError:
    portal_id = 'books' 

if not app.hasObject(portal_id):
    print "Can't find a plone site with '%s' as id." % portal_id
    print "Please specify the id of your plone site as the first argument "
    print "to this script."
    print "Usage: <instancehome>/bin/instance run %s <id>" % sys.argv[0]
    sys.exit(1)


portal = app[portal_id]

# we assume there is an admin user
app = makerequest.makerequest(app)
user = app.acl_users.getUser('admin')
newSecurityManager(None, user.__of__(app.acl_users))

# install latest version
portal.portal_quickinstaller.reinstallProducts(['UpfrontAccounting'])

for brain in portal.portal_catalog.unrestrictedSearchResults(
        portal_type='CashBook'):
    print 'Upgrading %s' % brain.getPath()

    cashbook = brain.getObject()
    event = ObjectAddedEvent(cashbook, cashbook.aq_parent, cashbook.getId())
    notify(event)

    # copy attributes from cashbook
    cashbook.entries._balances = cashbook._balances
    cashbook.entries._id_counter = cashbook._id_counter
    cashbook.entries._tree = cashbook._tree
    cashbook.entries._count = cashbook._count
    cashbook.entries._mt_index = cashbook._mt_index
    cashbook.entries._positionId = cashbook._positionId
    cashbook.entries._idPosition = cashbook._idPosition

    # delete attributes from cashbook
    del cashbook._balances
    del cashbook._tree
    del cashbook._count
    del cashbook._mt_index
    del cashbook._positionId
    del cashbook._idPosition

    # remove opening balance from _balances
    cashbook.entries.removeEntryBalance(0)

    # index entries in cashbook_catalog
    for entry in cashbook.entries.objectValues():
        entry.reindexObject()

transaction.commit()
