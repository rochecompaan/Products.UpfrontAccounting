from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction
from invoice import InvoiceItemsView

class QuoteItemsView(PloneKSSView):

    def _render_table(self):
        content = self.macroContent('quote_edit/macros/itemstable')
        core = self.getCommandSet('core')
        core.replaceHTML('#InvoiceItems', content)

    @kssaction
    def addItem(self):
        # Add a new item
        itemid = '%02d' % (len(self.context.objectValues('InvoiceItem')) + 1)
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
        content = self.macroContent('quote_edit/macros/invoicetotals')
        core.replaceHTML('#InvoiceTotals', content)

