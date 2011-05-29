""" Run this script to add areview state index on CashBook
"""
import sys
import transaction
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from zope.index.field import FieldIndex

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

for brain in portal.portal_catalog.unrestrictedSearchResults(
        portal_type='CashBook'):
    print 'Upgrading %s' % brain.getPath()

    cashbook = brain.getObject()
    cashbook._review_state_index = FieldIndex()

    for entry in cashbook.objectValues():
        cashbook.indexReviewState(entry)


transaction.commit()
