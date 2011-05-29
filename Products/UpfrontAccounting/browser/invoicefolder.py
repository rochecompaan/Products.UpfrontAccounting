from Products.Five import BrowserView
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.UpfrontAccounting.interfaces import IMailInvoice

class InvoiceFolderView(BrowserView):
    """ 
    """

    def __call__(self, *args, **kw):
        """ we render the template except when we are importing and
            writing progress to the response.
        """
        if self.request.has_key('postInvoices'):
            self.postPendingInvoices()
        elif self.request.has_key('mailInvoices'):
            self.mailInvoices()
        else:
            return self.index()


    def name(self):
        return self.__name__

    def states(self):
        """ return transaction workflow states
        """
        wtool = getToolByName(self.context, 'portal_workflow')        
        return wtool.invoice_workflow.states.objectValues()

    def batched_invoices(self):
        """ Return invoices as batch
        """
        request = self.request
        b_size = request.get('b_size', 100)
        filter = {}
        has_key = request.has_key
        if has_key('start_date') and request.get('start_date') is not None \
            and has_key('end_date') and request.get('end_date') is not None:
            filter = {
                'getInvoiceDate': {'query': [self.request.get('start_date'),
                                        self.request.get('end_date')],
                              'range': 'min:max'},
                }
        elif has_key('start_date') and request.get('start_date') is not None:
            filter = {
                'getInvoiceDate': {'query': [self.request.get('start_date')],
                              'range': 'min'},
                }
        elif has_key('end_date') and request.get('end_date') is not None:
            filter = {
                'getInvoiceDate': {'query': [self.request.get('end_date')],
                              'range': 'max'}
                }

        self.filter = filter
        if has_key('review_state'):
            filter['review_state'] = self.request.get('review_state') 

        filter['sort_on'] = 'getId'

        invoices = self.context.invoice_catalog(filter)
        b_start = self.request.get('b_start', (len(invoices)/100) * 100)
        return Batch(invoices, b_size, int(b_start), orphan=1);

    def postPendingInvoices(self):
        """ Post pending invoices
        """
        self.context.postPendingInvoices()
        self.request.RESPONSE.redirect(self.context.absolute_url())

    def mailInvoices(self):
        """ Mail selected invoices
        """
        for path in self.request.get('paths', []):
            invoice = self.context.restrictedTraverse(path)
            IMailInvoice(invoice).send()
        self.request.RESPONSE.redirect(self.context.absolute_url())
        self.context.plone_utils.addPortalMessage(
            _(u'Invoices mailed successfully'))
