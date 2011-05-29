from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

class InvoiceItemsView(PloneKSSView):

    def _render_table(self):
        content = self.macroContent('invoice_edit/macros/itemstable')
        core = self.getCommandSet('core')
        core.replaceHTML('#InvoiceItems', content)

    @kssaction
    def editInvoiceCurrency(self, currency):
        """ Change the invoice currency on all invoice items.
        """
        self.context.edit(InvoiceCurrency=currency)
        for item in self.context.objectValues('InvoiceItem'):
            amount = item.getRate().amount()
            item.edit(Rate='%s %s' % (currency, amount))
        self._render_table()

        # update invoice totals
        content = self.macroContent('invoice_edit/macros/invoicetotals')
        core = self.getCommandSet('core')
        core.replaceHTML('#InvoiceTotals', content)

    @kssaction
    def addItem(self):
        # Add a new item
        itemid = self.context.generateUniqueId('InvoiceItem')
        self.context.invokeFactory(type_name="InvoiceItem", id=itemid)
        self._render_table()

    @kssaction
    def delItem(self, itemId):
        # delete item
        self.context.manage_delObjects(itemId)
        self._render_table()

    @kssaction
    def editItem(self, itemId):
        item = self.context[itemId]
        values = {}
        for fieldName in ('description', 'Unit', 'Quantity', 'Rate'):
            varname = 'item.%s.%s' % (itemId, fieldName)
            value = self.request.get(varname)
            if value:
                values[fieldName] = value
        item.edit(**values)

        core = self.getCommandSet('core')

        # update item total
        itemtotal = str(item.getTotal())
        core.replaceInnerHTML('#item-%s-total' % itemId, itemtotal)

        # update invoice totals
        content = self.macroContent('invoice_edit/macros/invoicetotals')
        core.replaceHTML('#InvoiceTotals', content)
