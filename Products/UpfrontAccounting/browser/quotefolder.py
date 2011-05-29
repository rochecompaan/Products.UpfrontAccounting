from Products.Five import BrowserView
from zope.interface import implements, Interface
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

class CreateQuoteView(BrowserView):

    def createObject(self):
        """ 
        """
        return self.request.response.redirect('quote_add')

    def getQuote(self):
        id = self.context.generateUniqueId('Quote')
        return self.context.restrictedTraverse('portal_factory/Quote/%s'%id)

    def getCustomer(self):
        id = self.context.accounts.generateUniqueId('CustomerAccount')
        return self.context.accounts.restrictedTraverse(
            'portal_factory/CustomerAccount/%s'%id)

    def getPerson(self):
        id = self.context.generateUniqueId('Person')
        return self.context.restrictedTraverse('portal_factory/Person/%s'%id)

    def getErrors(self):
        #options/state/getErrors
        return {}

    def createQuote(self):
        request = self.request
        context = self.context
        accounts = self.context.accounts

        if request.customer_type == 'new':
            # create organisastion
            customer_id = accounts.generateUniqueId('CustomerAccount')
            accounts.invokeFactory(type_name='CustomerAccount',
                id=account_id)
            customer = accounts._getOb(account_id)
            customer.processForm(values=request.get('CustomerAccount'))
            customer_uid = customer.UID()

            # create person
            person_id = customer.generateUniqueId('Person')
            customer.invokeFactory(type_name='Person', id=person_id)
            person = customer._getOb(person_id)
            person.processForm(values=request.get('Person'))

        elif request.customer_type == 'existing':
            customer_uid = request.CustomerAccount
            

        quote_id = context.generateUniqueId('Quote')

        # set company on session as reference
        session = None
        sdm = getToolByName(context, 'session_data_manager', None)
        if sdm is not None:
            session = sdm.getSessionData(create=0)
            if session is None:
                session = sdm.getSessionData(create=1)
        session.set(quote_id, {'CustomerAccount': customer_uid})

        # Create and redirect to quote
        quote = context.restrictedTraverse('portal_factory/Quote/' + quote_id)
        return context.REQUEST.RESPONSE.redirect(
            '%s/edit' % quote.absolute_url())

