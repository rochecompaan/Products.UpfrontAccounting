from Products.Five import BrowserView
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.utils import getToolByName

class ListInvoiceTemplatesView(BrowserView):
    """ 
    """

    def name(self):
        return self.__name__

    def states(self):
        """ return transaction workflow states
        """
        wtool = getToolByName(self.context, 'portal_workflow')        
        return wtool.invoice_workflow.states.objectValues()

    def invoicetemplates(self):
        """ Return invoices as batch
        """
        request = self.request
        b_size = request.get('b_size', 100)
        invoicetemplates = self.context.objectValues()
        b_start = self.request.get('b_start', 0)
        return Batch(invoicetemplates, b_size, int(b_start), orphan=1);

