from Products.CMFCore.utils import getToolByName
from csvimporter import CSVImporter
from Products.UpfrontAccounting.content.InvoiceItem import InvoiceItem

class InvoiceTemplateImporter(CSVImporter):
    """ Specialise CSVImporter to import invoicetemplate csv files
    """

    def _addObject(self, row):
        """ use row data from CSV file and create an object from it
        """
        if row.has_key('InvoiceTemplate.id'):
            invoice_id = row.get('InvoiceTemplate.id')
        else:
            invoice_id = self.context.generateUniqueId(
                type_name='InvoiceTemplate')

        invoicetemplate_values = {}
        item_values = {}

        # split invoicetemplate and item data
        for key, value in row.items():
            content_type, fieldname = key.split('.')
            if content_type == 'InvoiceTemplate':
                invoicetemplate_values[fieldname] = value
            elif content_type == 'InvoiceItem':
                item_values[fieldname] = value

        # create invoicetemplate if it doesn't exist
        if not self.context.hasObject(invoice_id):
            self.context.invokeFactory(type_name='InvoiceTemplate',
                id=invoicetemplate_values['id'])
            invoicetemplate = self.context[invoice_id]
            self._convert_references(invoicetemplate_values, invoicetemplate)
            invoicetemplate.edit(**invoicetemplate_values)
        else:
            invoicetemplate = self.context[invoice_id]

        # create invoice item
        del item_values['id']
        item_id = invoicetemplate.generateUniqueId('InvoiceItem')
        item = InvoiceItem(item_id)
        invoicetemplate._setObject(item_id, item)
        item = invoicetemplate._getOb(item_id)

        item.edit(**item_values)
