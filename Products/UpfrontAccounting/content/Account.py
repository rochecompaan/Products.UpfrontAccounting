# -*- coding: utf-8 -*-
#
# File: Account.py
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
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.FinanceFields.MoneyField import MoneyField
from Products.FinanceFields.MoneyWidget import MoneyWidget
from BTrees.IOBTree import IOBTree
from DocumentTemplate import sequence
from Products.FinanceFields.Money import Money
from upfront.simplereferencefield import SimpleReferenceField

##code-section module-header #fill in your manual code here
from zope.interface import classImplements
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance
from DateTime.DateTime import DateTime
from Products.CMFCore import permissions
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='Opened',
        widget=DateTimeField._properties['widget'](
            label='Opened',
            label_msgid='UpfrontAccounting_label_Opened',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    StringField(
        name='AccountType',
        widget=SelectionWidget(
            label="Account type",
            label_msgid='UpfrontAccounting_label_AccountType',
            i18n_domain='UpfrontAccounting',
        ),
        vocabulary=ACCOUNT_TYPES,
    ),
    StringField(
        name='AccountNumber',
        widget=StringField._properties['widget'](
            label="Account number",
            label_msgid='UpfrontAccounting_label_AccountNumber',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    ReferenceField(
        name='SubsidiaryLedger',
        widget=ReferenceBrowserWidget(
            label="Subsidiary Ledger",
            visible=False,
            label_msgid='UpfrontAccounting_label_SubsidiaryLedger',
            i18n_domain='UpfrontAccounting',
        ),
        allowed_types= ('SubsidiaryLedger', 'DebtorLedger', 'CreditorLedger', 'CashBook'),
        relationship="AccountSubsidiaryLedger",
    ),
    SimpleReferenceField(
        name='TransactionEntries',
        widget=SimpleReferenceField._properties['widget'](
            visible=False,
            label='Transactionentries',
            label_msgid='UpfrontAccounting_label_TransactionEntries',
            i18n_domain='UpfrontAccounting',
        ),
        storage=AnnotationStorage(),
        multiValued=True,
        relationship="AccountTransaciontEntries",
    ),
    MoneyField(
        name='Balance',
        widget=MoneyWidget(
            visible={'edit': 'hidden', 'view': 'visible'},
            label='Balance',
            label_msgid='UpfrontAccounting_label_Balance',
            i18n_domain='UpfrontAccounting',
        ),
        required=True,
    ),
    LinesField(
        name='BankStatementText',
        widget=LinesField._properties['widget'](
            label="Bank Statement Text",
            description="The text to match this account when importing a bank statement",
            label_msgid='UpfrontAccounting_label_BankStatementText',
            description_msgid='UpfrontAccounting_help_BankStatementText',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    BooleanField(
        name='TaxIncludedInCashBookEntries',
        widget=BooleanField._properties['widget'](
            label="Sales tax included in cash book entries",
            description="Sales tax is included in the amount. This setting will be the default on cashbook entries but can be modified afterwards.",
            label_msgid='UpfrontAccounting_label_TaxIncludedInCashBookEntries',
            description_msgid='UpfrontAccounting_help_TaxIncludedInCashBookEntries',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    MoneyField(
        name='OpeningBalance',
        widget=MoneyField._properties['widget'](
            label="Opening Balance",
            label_msgid='UpfrontAccounting_label_OpeningBalance',
            i18n_domain='UpfrontAccounting',
        ),
    ),
    BooleanField(
        name='Active',
        default=True,
        widget=BooleanField._properties['widget'](
            description="Indicates if account is active",
            label='Active',
            label_msgid='UpfrontAccounting_label_Active',
            description_msgid='UpfrontAccounting_help_Active',
            i18n_domain='UpfrontAccounting',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Account_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Account(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IAccount)

    meta_type = 'Account'
    _at_rename_after_creation = True

    schema = Account_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def __init__(self, oid, **kwargs):
        BaseFolder.__init__(self, oid, **kwargs)
        self._daily_balances = IOBTree()
        self._closing_balances = IOBTree()

    def setOpeningBalance(self, value, **kw):
        """ Update opening balance.
        """
        if value is None:
            return

        balances = self._daily_balances
        zero = IZeroMoneyInstance(self)()
        curbalance = balances.get(0, zero)
        effective_date = DateTime(0)
        key = self._get_key(effective_date)

        balances[key] = value

        # update the balance for all entries
        difference = value - curbalance
        self._update_daily_balances(difference, effective_date)

        # update the opening balance
        field = self.Schema().get('OpeningBalance')
        result = field.set(self, value, **kw)

        # update balance on REQUEST
        newbalance = self.getBalance() + difference
        self.setBalance(newbalance)

    security.declareProtected(ManageTransactions, 'creditAccount')
    def creditAccount(self, amount, effective_date):
        """ credit account """
        new_balance = self.getBalance() - amount
        self.setBalance(new_balance)
        self._update_daily_balances(-amount, effective_date)
        self.reindexObject()
        if self.aq_parent.portal_type == 'Account':
            self.aq_parent.creditAccount(amount, effective_date)

    security.declareProtected(ManageTransactions, 'debitAccount')
    def debitAccount(self, amount, effective_date):
        """ debit account """
        new_balance = self.getBalance() + amount
        self.setBalance(new_balance)
        self._update_daily_balances(amount, effective_date)
        self.reindexObject()
        if self.aq_parent.portal_type == 'Account':
            self.aq_parent.debitAccount(amount, effective_date)

    security.declareProtected(ManageAccounts, 'getBalanceForDate')
    def getBalanceForDate(self, date):
        """ Return the balance for a given date """
        key = self._get_key(date)
        keys = self._daily_balances.keys(0, key)
        if keys:
            return self._daily_balances[keys[-1]]
        else:
            return IZeroMoneyInstance(self)()

    security.declareProtected(ManageAccounts, 'setClosingBalanceForDate')
    def setClosingBalanceForDate(self, date):
        """ Record a closing balance for a given date
        """
        key = self._get_key(date)
        if self._closing_balances.has_key(key):
            raise RuntimeError, 'Duplicate closing balance'
        self._closing_balances[key] = self.getBalanceForDate(date)

    security.declareProtected(ManageAccounts, 'getClosingBalanceForDate')
    def getClosingBalanceForDate(self, date):
        """ Return the closing balance for a given date """
        key = self._get_key(date)
        zero = IZeroMoneyInstance(self)()
        return self._closing_balances.get(key, zero)

    def _get_key(self, date):
        # strip time when computing key
        date = DateTime(date.Date())
        return int(date)

    def _update_daily_balances(self, amount, effective_date):
        key = self._get_key(effective_date)
        if len(self._daily_balances) == 0:
            self._daily_balances[key] = amount
        else:
            maxkey = self._daily_balances.maxKey()
            # insert the key if it is new. initialize the value with the
            # last balance if it is not the first key
            if not self._daily_balances.has_key(key):
                previous_keys = self._daily_balances.keys(0, key)
                if previous_keys:
                    previous_key = previous_keys[-1]
                    self._daily_balances[key] = \
                        self._daily_balances[previous_key]
                else:
                    self._daily_balances[key] = IZeroMoneyInstance(self)()

            if key < maxkey:
                # update all values between key and maxkey
                for k in self._daily_balances.keys(key, maxkey):
                    balance = self._daily_balances[k] + amount
                    self._daily_balances[k] = balance
            else:
                balance = self._daily_balances[key] + amount
                self._daily_balances[key] = balance

    security.declareProtected(permissions.View, 'getTransactionEntriesAndBalances')
    def getTransactionEntriesAndBalances(self, period=None):
        """ Return transaction entries and their balances """
        if period:
            startdate = DateTime() - period

        entries = self.getTransactionEntries()
        if not entries:
            return []

        def sortfunc(x, y):
            """ Sort on TransactionDate and then on the transaction id
            """
            xdate = x.getTransactionDate().Date()
            ydate = y.getTransactionDate().Date()
            i = cmp(xdate, ydate)
            if i == 0:
                return cmp(x.aq_parent.getId(), y.aq_parent.getId())
            else:
                return i

        entries.sort(sortfunc)

        balance = self.getOpeningBalance()
        if not balance:
            balance = Money('0.0', self.getAccountingCurrency())
        entries_with_balances = []

        for entry in entries:
            if entry.getDebitCredit() == DEBIT:
                balance = balance + entry.getAmount()
            else:
                balance = balance - entry.getAmount()
            if period and entry.getTransactionDate() < startdate:
                continue
            entries_with_balances.append(
                entryproxy(entry, balance)
            )
        return entries_with_balances



registerType(Account, PROJECTNAME)
# end of class Account

##code-section module-footer #fill in your manual code here

# Add IAccountFolder to interfaces Account implements
classImplements(Account, interfaces.IAccount, interfaces.IAccountFolder)

class entryproxy:
    __allow_access_to_unprotected_subobjects__=1
    def __init__(self, entry, balance):
        self.entry = entry
        self.balance = balance

    def __getattr__(self, name):
        if name == 'balance':
            return self.balance
        elif name == 'absolute_url':
            return getattr(self.entry.aq_parent, name)
        else:
            return getattr(self.entry, name)

from AccessControl import allow_class
allow_class(entryproxy)

def getBankStatementTextAsString(obj, **kwargs):
    """ Return BankStatementText lines field as text for indexing
    """
    return '\n'.join(obj.getBankStatementText())

from Products.CMFPlone.CatalogTool import registerIndexableAttribute
registerIndexableAttribute('BankStatementTextAsString',
    getBankStatementTextAsString)
##/code-section module-footer



