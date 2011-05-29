from DateTime import DateTime
from Products.Five import BrowserView

class RecurringInvoices(BrowserView):
    """ Create invoices from invoice templates
    """

    def __call__(self, *args, **kw):
        if self.request.has_key('submit'):
            self.create_invoices()
        else:
            return self.index()

    def create_invoices(self):
        invoicedate = DateTime(self.request.get('recurring_invoices_date'))
        ledger = self.context.getLedger()
        templates = ledger.invoicetemplates
        for template in templates.objectValues('InvoiceTemplate'):
            invoice_id = str(ledger.getNextInvoiceNumber())
            self.context.invokeFactory(id=invoice_id, type_name='Invoice')
            invoice = getattr(self.context, invoice_id)
            invoice.edit(
                CustomerAccount=template.getCustomerAccount(),
                title='%s (%s, %s)' % (
                    invoice_id, invoicedate.Month(), invoicedate.year()),
                InvoiceDate=invoicedate,
                CalculateTax=template.getCalculateTax(),
                InvoiceCurrency=template.getInvoiceCurrency(),
                ExchangeRate=template.getExchangeRate(),
                Notes=template.getNotes(),
            )
            cp = template.manage_copyObjects(ids=template.objectIds(
                'InvoiceItem'))
            invoice.manage_pasteObjects(cp)
            # update the id counter
            invoice._id_counter = template._id_counter

        return self.request.RESPONSE.redirect(self.context.absolute_url())
