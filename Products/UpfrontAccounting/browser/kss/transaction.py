from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from plone.memoize import view
from Products.UpfrontAccounting.browser.utils import ListAccounts
from Products.CMFCore.utils import getToolByName

class TransactionView(PloneKSSView):

    def editTransaction(self):
        self.context.processForm(REQUEST=self.request)

    def _render_table(self):
        # build HTML
        content = self.macroContent('transaction_edit/macros/entries',
                                    transaction=self.context)

        # KSS specific calls
        core = self.getCommandSet('core')
        core.replaceHTML('#TransactionTable', content)

    def _render_amount(self, entry):
        # build HTML
        content = self.macroContent('transaction_edit/macros/amount', 
                    entry=entry)

        # KSS specific calls
        core = self.getCommandSet('core')
        core.replaceHTML('#amount_%s' % entry.getId(), content)

    @kssaction
    def addEntry(self):
        # Add a new entry
        entryid = self.context.generateUniqueId('TransactionEntry')
        portal_types = getToolByName(self.context, 'portal_types')
        portal_types.constructContent('TransactionEntry',
                                        self.context,
                                        entryid,)
        self._render_table()

    @kssaction
    def delEntry(self, entryId):
        # delete entry
        self.context._delObject(entryId)
        self._render_table()

    @kssaction
    def editField(self, entryId, fieldName):
        entry = self.context[entryId]
        values = {}
        varname = 'entry.%s.%s' % (entryId, fieldName)
        value = self.request.get(varname)

        uid_title_map = self._uid_title_map()
        if fieldName == 'Account':
            value = uid_title_map.get(value)

        if value:
            values[fieldName] = value
        entry.edit(**values)
        if fieldName == 'Amount':
            self._render_amount(entry)

    @view.memoize
    def _uid_title_map(self):
        view = ListAccounts(self.context, self.request)
        uidmap = {}
        for account in view.list():
            option = account.Title()
            uidmap[option] = account.UID()
        return uidmap


