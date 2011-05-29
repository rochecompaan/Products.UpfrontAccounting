from Products.Five import BrowserView
from zope.interface import implements, Interface
from DateTime import DateTime
from Products.UpfrontAccounting.interfaces import IAccountList
from Products.CMFPlone import Batch
from Products.CMFCore.utils import getToolByName

class ListCreditNotesView(BrowserView):

    def name(self):
        return self.__name__

    def batch(self):
        """ Return creditnotes as batch
        """
        request = self.request
        b_size = request.get('b_size', 100)
        filter = {}
        has_key = request.has_key
        if has_key('start_date') and request.get('start_date') is not None \
            and has_key('end_date') and request.get('end_date') is not None:
            filter = {
                'getCreditNoteDate': {
                    'query': [self.request.get('start_date'),
                                        self.request.get('end_date')],
                    'range': 'min:max'},
                }
        elif has_key('start_date') and request.get('start_date') is not None:
            filter = {
                'getCreditNoteDate': {
                    'query': [self.request.get('start_date')],
                    'range': 'min'},
                }
        elif has_key('end_date') and request.get('end_date') is not None:
            filter = {
                'getCreditNoteDate': {
                    'query': [self.request.get('end_date')],
                    'range': 'max'}
                }

        self.filter = filter
        if has_key('review_state'):
            filter['review_state'] = self.request.get('review_state') 

        filter['sort_on'] = 'getCreditNoteDate'

        creditnotes = self.context.objectValues()
        b_start = self.request.get('b_start', (len(creditnotes)/100) * 100)
        return Batch(creditnotes, b_size, int(b_start), orphan=1);

