# -*- coding: utf-8 -*-
#
# File: UpfrontAccounting.py
#
# Copyright (c) 2010 by Upfront Systems
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Upfront Systems <info@upfrontsystems.co.za>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
##code-section config-head #fill in your manual code here
##/code-section config-head


PROJECTNAME = "UpfrontAccounting"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))
ADD_CONTENT_PERMISSIONS = {
    'Account': 'UpfrontAccounting: Add Account',
    'AccountFolder': 'UpfrontAccounting: Add AccountFolder',
    'AccountingFolder': 'UpfrontAccounting: Add AccountingFolder',
    'Ledger': 'UpfrontAccounting: Add Ledger',
    'CashBook': 'UpfrontAccounting: Add CashBook',
    'SubsidiaryLedger': 'UpfrontAccounting: Add SubsidiaryLedger',
    'CustomerLedger': 'UpfrontAccounting: Add CustomerLedger',
    'SupplierLedger': 'UpfrontAccounting: Add SupplierLedger',
    'TransactionFolder': 'UpfrontAccounting: Add TransactionFolder',
    'Transaction': 'UpfrontAccounting: Add Transaction',
    'TransactionEntry': 'UpfrontAccounting: Add TransactionEntry',
    'CashBookEntry': 'UpfrontAccounting: Add CashBookEntry',
    'CustomerAccountFolder': 'UpfrontAccounting: Add CustomerAccountFolder',
    'CustomerAccount': 'UpfrontAccounting: Add CustomerAccount',
    'InvoiceFolder': 'UpfrontAccounting: Add InvoiceFolder',
    'Invoice': 'UpfrontAccounting: Add Invoice',
    'InvoiceItem': 'UpfrontAccounting: Add InvoiceItem',
    'QuoteFolder': 'UpfrontAccounting: Add QuoteFolder',
    'Quote': 'UpfrontAccounting: Add Quote',
    'CreditNoteFolder': 'UpfrontAccounting: Add CreditNoteFolder',
    'CreditNote': 'UpfrontAccounting: Add CreditNote',
    'SubsidiaryAccount': 'UpfrontAccounting: Add SubsidiaryAccount',
    'SubsidiaryAccountFolder': 'UpfrontAccounting: Add SubsidiaryAccountFolder',
    'InvoiceTemplateFolder': 'UpfrontAccounting: Add InvoiceTemplateFolder',
    'InvoiceTemplate': 'UpfrontAccounting: Add InvoiceTemplate',
    'OrderedBTreeContainer': 'UpfrontAccounting: Add OrderedBTreeContainer',
    'CashBookEntryFolder': 'UpfrontAccounting: Add CashBookEntryFolder',
}

setDefaultRoles('UpfrontAccounting: Add Account', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add AccountFolder', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add AccountingFolder', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add Ledger', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add CashBook', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add SubsidiaryLedger', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add CustomerLedger', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add SupplierLedger', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add TransactionFolder', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add Transaction', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add TransactionEntry', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add CashBookEntry', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add CustomerAccountFolder', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add CustomerAccount', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add InvoiceFolder', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add Invoice', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add InvoiceItem', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add QuoteFolder', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add Quote', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add CreditNoteFolder', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add CreditNote', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add SubsidiaryAccount', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add SubsidiaryAccountFolder', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add InvoiceTemplateFolder', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add InvoiceTemplate', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add OrderedBTreeContainer', ('Manager','Owner'))
setDefaultRoles('UpfrontAccounting: Add CashBookEntryFolder', ('Manager','Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
STATEMENT_CSV_KEY = 'statement_csv_file' # for saving statement csv data in session variable
STATEMENT_CSV_HEADERS_KEY = 'statement_csv_headers' # for saving statement csv data in session variable
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.UpfrontAccounting.AppConfig import *
except ImportError:
    pass
