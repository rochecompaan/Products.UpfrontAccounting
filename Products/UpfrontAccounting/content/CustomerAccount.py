# -*- coding: utf-8 -*-
#
# File: CustomerAccount.py
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
from Products.UpfrontAccounting.content.SubsidiaryAccount import SubsidiaryAccount
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.UpfrontAccounting.config import *

##code-section module-header #fill in your manual code here
from organisationschema import organisation_schema
##/code-section module-header

schema = Schema((

    BooleanField(
        name='TaxIncluded',
        default="False",
        widget=BooleanField._properties['widget'](
            label="Tax Included",
            description="Sales tax is included in transactions for this account. This field is only used as a default and can be modified afterwards",
            label_msgid='UpfrontAccounting_label_TaxIncluded',
            description_msgid='UpfrontAccounting_help_TaxIncluded',
            i18n_domain='UpfrontAccounting',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CustomerAccount_schema = BaseSchema.copy() + \
    getattr(SubsidiaryAccount, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
AccountNumber = CustomerAccount_schema['AccountNumber']
AccountNumber.widget.visible = {'edit': 'hidden', 'view': 'invisible'}

CustomerAccount_schema = CustomerAccount_schema.copy() + \
    organisation_schema.copy()

# relabel title field and delete organisation name from schema
title_field = CustomerAccount_schema['title']
title_field.widget.label = 'Customer Name'
title_field.widget.label_msgid = 'label_customername',
del CustomerAccount_schema['OrganisationName']
##/code-section after-schema

class CustomerAccount(SubsidiaryAccount, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ICustomerAccount)

    meta_type = 'CustomerAccount'
    _at_rename_after_creation = True

    schema = CustomerAccount_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def getAccountNumber(self):
        """ return 'id' as AccountNumber """
        return self.getId()



registerType(CustomerAccount, PROJECTNAME)
# end of class CustomerAccount

##code-section module-footer #fill in your manual code here
##/code-section module-footer



