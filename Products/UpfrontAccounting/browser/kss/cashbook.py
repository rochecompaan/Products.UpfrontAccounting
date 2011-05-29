from types import StringTypes
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from DateTime import DateTime
from Products.FinanceFields.Money import Money
from Products.CMFCore.utils import getToolByName
from Products.UpfrontAccounting.browser.utils import ListAccounts
from plone.memoize import view

class CashbookView(PloneKSSView):

    def _render_table(self, lastpage=False):
        if lastpage:
            count = len(self.context.getPendingEntries())
            content = self.macroContent(
                'cashbookentryfolder_edit/macros/entries',
                b_start=(count / 50) * 50)
        else:
            content = self.macroContent(
                'cashbookentryfolder_edit/macros/entries')
            
        core = self.getCommandSet('core')
        core.replaceHTML('#CashbookEntries', content)

    def _render_amount(self, entry):
        # build HTML
        content = self.macroContent(
            'cashbookentryfolder_edit/macros/amount', entry=entry)

        # KSS specific calls
        core = self.getCommandSet('core')
        core.replaceHTML('#amount_%s' % entry.getId(), content)

    def _render_totals(self):
        core = self.getCommandSet('core')

        # list of totalIds that needs to be updated
        ids = [f.strip('entry.Amount') for f in self.request.form.keys()
               if 'Amount' in f]

        # build HTML
        for id in ids:
            entry = self.context[id]
            content = self.macroContent(
                'cashbookentryfolder_edit/macros/balance', 
                entry=entry)
            # KSS specific calls
            core.replaceHTML('#balance_%s' % entry.getId(), content)

    @kssaction
    def addEntry(self):
        # Add a new item
        itemid = self.context.generateUniqueId(type_name='CashBookEntry')
        zeroMoneyInstance = Money('0.0', self.context.getAccountingCurrency())
        portal_types = getToolByName(self.context, 'portal_types')
        portal_types.constructContent('CashBookEntry', self.context, itemid)
                                        
        # select the same account as the last entry in the cashbook - reduces
        # having to select the same entry all the time
        self.context[itemid].edit(
            Date=DateTime().earliestTime(), 
            Amount=zeroMoneyInstance,
            )
        self._render_table(lastpage=True)

    @kssaction
    def delEntry(self, entryId):
        # delete item - events fire to delete the entry from the Cashbook
        # balance and position fields
        self.context.manage_delObjects(entryId)
        self._render_table()

    @kssaction
    def editField(self, entryId, fieldName):
        entry = self.context[entryId]
        values = {}
        varname = 'entry.%s.%s' % (entryId, fieldName)

        value = self.request.get(varname)
        if isinstance(value, StringTypes):
            value = value.strip()
        uid_title_map = self._uid_title_map()
        if fieldName == 'Account':
            value = uid_title_map.get(value)

        if fieldName == 'TaxIncluded':
            if value is None:
                value = False
            else:
                value = True

        if value is not None:
            values[fieldName] = value
            entry.edit(**values)

        if fieldName == 'Amount':
            self._render_amount(entry)
            self._render_totals()

    @view.memoize
    def _uid_title_map(self):
        view = ListAccounts(self.context, self.request)
        uidmap = {}
        for account in view.list():
            option = account.Title()
            uidmap[option] = account.UID()
        return uidmap


