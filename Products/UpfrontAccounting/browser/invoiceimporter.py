from Products.CMFCore.utils import getToolByName
from csvimporter import CSVImporter
from Products.UpfrontAccounting.content.InvoiceItem import InvoiceItem

class InvoiceImporter(CSVImporter):
    """ Specialise CSVImporter to import invoice csv files
    """

    def _addObject(self, row):
        """ use row data from CSV file and create an object from it
        """
        if row.has_key('Invoice.id'):
            invoice_id = row.get('Invoice.id')
        else:
            invoice_id = self.context.generateUniqueId(type_name='Invoice')

        invoice_values = {}
        item_values = {}

        # split invoice and item data
        for key, value in row.items():
            content_type, fieldname = key.split('.')
            if content_type == 'Invoice':
                invoice_values[fieldname] = value
            elif content_type == 'InvoiceItem':
                item_values[fieldname] = value

        # create invoice if it doesn't exist
        if not self.context.hasObject(invoice_id):
            self.context.invokeFactory(type_name='Invoice',
                id=invoice_values['id'])
            invoice = self.context[invoice_id]
            self._convert_references(invoice_values, invoice)
            invoice.edit(**invoice_values)
        else:
            invoice = self.context[invoice_id]

        # create invoice item
        del item_values['id']
        item_id = invoice.generateUniqueId('InvoiceItem')
        item = InvoiceItem(item_id)
        invoice._setObject(item_id, item)
        item = invoice._getOb(item_id)

        item.edit(**item_values)
