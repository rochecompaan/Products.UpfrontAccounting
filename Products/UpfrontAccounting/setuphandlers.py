# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2010 by Upfront Systems
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Upfront Systems <info@upfrontsystems.co.za>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('UpfrontAccounting: setuphandlers')
from Products.UpfrontAccounting.config import PROJECTNAME
from Products.UpfrontAccounting.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
from Products.Archetypes import listTypes
from interfaces import ICashbookView
from zope.interface import alsoProvides, noLongerProvides
##/code-section HEAD

def isNotUpfrontAccountingProfile(context):
    return context.readDataFile("UpfrontAccounting_marker.txt") is None

def installQIDependencies(context):
    """This is for old-style products using QuickInstaller"""
    if isNotUpfrontAccountingProfile(context): return 
    logger.info("installQIDependencies starting")
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')

    for dependency in DEPENDENCIES:
        if qi.isProductInstalled(dependency):
            logger.info("   re-Installing QI dependency %s:" % dependency)
            qi.reinstallProducts([dependency])
            transaction.savepoint() # is a savepoint really needed here?
            logger.debug("   re-Installed QI dependency %s:" % dependency)
        else:
            if qi.isProductInstallable(dependency):
                logger.info("   installing QI dependency %s:" % dependency)
                qi.installProduct(dependency)
                transaction.savepoint() # is a savepoint really needed here?
                logger.debug("   installed dependency %s:" % dependency)
            else:
                logger.info("   QI dependency %s not installable" % dependency)
                raise "   QI dependency %s not installable" % dependency
    logger.info("installQIDependencies finished")



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotUpfrontAccountingProfile(context): return 
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotUpfrontAccountingProfile(context): return



##code-section FOOT
def setupHideMetaTypesFromNavigations(context):
    """hide selected classes in the search form"""
    if isNotUpfrontAccountingProfile(context): return 
    # XXX use https://svn.plone.org/svn/collective/DIYPloneStyle/trunk/profiles/default/properties.xml
    site = context.getSite()
    portalProperties = getToolByName(site, 'portal_properties')
    navProps = getattr(portalProperties, 'navtree_properties')
    for klass in ['Account', 'CustomerAccount', 'SupplierAccount', 'Transaction', 'TransactionEntry', 'CashBookEntry', 'Invoice', 'InvoiceItem', 'Quote', 'CreditNote', 'SubsidiaryAccount', 'InvoiceTemplate']:
        propertyid = 'metaTypesNotToList'
        lines = list(navProps.getProperty(propertyid) or [])
        if klass not in lines:
            lines.append(klass)
            navProps.manage_changeProperties(**{propertyid: lines})

def setupCatalogMultiplex(context):
    """ Configure CatalogMultiplex.

    explicitly add classes (meta_types)to be indexed in catalogs (white)
    or remove from indexing in a catalog (black)
    """
    if isNotUpfrontAccountingProfile(context): return 
    site = context.getSite()
    #dd#
    muliplexed = ['Transaction', 'TransactionEntry', 'CashBookEntry']

    atool = getToolByName(site, 'archetype_tool')
    catalogmap = {}
    catalogmap['Transaction'] = {}
    catalogmap['Transaction']['black'] = ['portal_catalog']
    catalogmap['TransactionEntry'] = {}
    catalogmap['TransactionEntry']['black'] = ['portal_catalog']
    catalogmap['CashBookEntry'] = {}
    catalogmap['CashBookEntry']['black'] = ['portal_catalog']
    catalogmap['Invoice'] = {}
    catalogmap['Invoice']['black'] = ['portal_catalog']
    catalogmap['InvoiceTemplate'] = {}
    catalogmap['InvoiceTemplate']['black'] = ['portal_catalog']
    catalogmap['InvoiceItem'] = {}
    catalogmap['InvoiceItem']['black'] = ['portal_catalog']

    for meta_type in catalogmap:
        submap = catalogmap[meta_type]
        atooltype = '%s:%s' % (PROJECTNAME, meta_type)
        current_catalogs = set([c.id for c in atool.getCatalogsByType(
            meta_type)])
        if 'white' in submap:
            for catalog in submap['white']:
                if getToolByName(site, catalog, False) is False:
                    raise AttributeError, 'Catalog "%s" does not exist!' % catalog
                current_catalogs.update([catalog])
        if 'black' in submap:
            for catalog in submap['black']:
                if catalog in current_catalogs:
                    current_catalogs.remove(catalog)
        atool.setCatalogsByType(meta_type, list(current_catalogs))

def setupAllowedContentTypes(context):
    """ Setup allowed_content_types
    """
    if isNotUpfrontAccountingProfile(context): return 

    site = context.getSite()
    pt = getToolByName(site, 'portal_types')

    folder_types = (
        ('AccountFolder', 'Account'),
        ('CustomerAccountFolder', 'CustomerAccount'),
        ('InvoiceFolder', 'Invoice'),
        ('Transaction', None),
        ('CashBook', None),
        )

    for folder, type in folder_types:
        f = getattr(pt, folder, None)
        f.allowed_content_types = (type,)
        if type is None:
            f.allowed_content_types = ()

##/code-section FOOT
