from Products.Five import BrowserView
from zope.interface import implements, Interface
from DateTime import DateTime
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFCore.utils import getToolByName

class ListTransactionsView(BrowserView):
    """ List transactions view
    """

    def __call__(self):
        if self.request.has_key('post_transactions'):
            self.post_transactions()
            self.request.response.redirect(self.name())
        else:
            return self.index()


    def name(self):
        return self.__name__

    def states(self):
        """ return transaction workflow states
        """
        wtool = getToolByName(self.context, 'portal_workflow')        
        return wtool.transaction_workflow.states.objectValues()

    def batched_transactions(self):
        """ Return transactions as batch
        """
        b_size = self.request.get('b_size', 20)
        filter = {}
        has_key = self.request.has_key
        if has_key('start_date') and has_key('end_date'):
            filter = {
                'effective': {'query': [self.request.get('start_date'),
                                        self.request.get('end_date')],
                              'range': 'min:max'},
                }
        elif has_key('start_date'):
            filter = {
                'effective': {'query': [self.request.get('start_date')],
                              'range': 'min'},
                }
        elif has_key('end_date'):
            filter = {
                'effective': {'query': [self.request.get('end_date')],
                              'range': 'min'}
                }

        if has_key('review_state'):
            filter['review_state'] = self.request.get('review_state') 

        filter['sort_on'] = 'effective'

        transactions = self.context.transaction_catalog(filter)
        b_start = self.request.get('b_start', (len(transactions)/20) * 20)
        return Batch(transactions, b_size, int(b_start), orphan=1);

    def post_transactions(self):
        """ Post all pending transactions
        """
        wtool = getToolByName(self.context, 'portal_workflow')        
        wf = wtool.transaction_workflow
        pending = []
        for brain in self.context.transaction_catalog(review_state='pending'):
            txn = brain.getObject()
            if wf.isActionSupported(txn, 'post'):
                pending.append(txn)

        for txn in pending:
            wtool.doActionFor(txn, 'post')
            txn.reindexObject()
